import FactoryDb
from QueriesFromDb import QueriesFromDb

import csv
from Bio import Entrez, SeqIO
from Bio.Seq import Seq
import pandas as pd


class PopulateDb():
    def populate_ARO(work_folder, origin_file, default_list):
        """It parses the elements of the first table (Card_Fact_Table) without duplicates. """
        with open(work_folder + origin_file) as tsv_aro:
            rd = csv.reader(tsv_aro, delimiter='\t')
            next(rd)
            for row in rd:
                obj = FactoryDb.AROs.get_unique(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
                default_list.append(obj)
        FactoryDb.session.commit()
        return default_list

    def populate_FASTA(default_list, fasta_table, card_fact_table):
        """It searches for the FASTA info of the DNA Accession numbers of the Card_Fact_Table and introduces it in the second table (Fasta_Table).
        It first checkes whether the info is already in the Fasta_Table. """
        parsed_entries = QueriesFromDb.return_query_as_list(QueriesFromDb.select_query('DNA_Accession', fasta_table))
        to_be_parsed_entries = QueriesFromDb.return_query_as_list(QueriesFromDb.select_query('DNA_Accession', card_fact_table))
        to_be_parsed_entries_clean = QueriesFromDb.find_not_parsed_files_general(to_be_parsed_entries, parsed_entries)
        for i in to_be_parsed_entries_clean:
            handle = Entrez.efetch(db='nuccore', id=i, rettype='fasta', retmode='text')
            for record in SeqIO.parse(handle, 'fasta'):
                fastafile = FactoryDb.FASTA.get_unique(record.id, record.seq, record.description)
                default_list.append(fastafile.DNA_Accession)
            FactoryDb.session.commit()
        #print("FASTA records added: ", default_list)

    def populate_CDS(default_list, cds_table, card_fact_table):
        """It searches for the info of the initial and final positions of the coding sequence (CDS) of the protein within the DNA sequence, using the DNA Accession number.
        It first checks whether the info is already in its table 'cds_table'. """

        parsed_entries = QueriesFromDb.return_query_as_list(QueriesFromDb.select_query('ARO_Accession, DNA_Accession, Protein_Accession', cds_table))
        to_be_parsed_entries = QueriesFromDb.return_query_as_list(QueriesFromDb.select_query('ARO_Accession, DNA_Accession, Protein_Accession', card_fact_table))
        to_be_parsed_entries_clean = QueriesFromDb.find_not_parsed_files_general(to_be_parsed_entries, parsed_entries)
        print("Pending entries: ", to_be_parsed_entries_clean)
        for i in to_be_parsed_entries_clean:
            print("Checking", i)
            handle = Entrez.efetch(db='nuccore', id=i[1], rettype='gb', retmode='text')
            for record in SeqIO.parse(handle, 'genbank'):
                for feature in record.features:
                    if feature.type == 'CDS':
                        try:
                            if str(feature.qualifiers['protein_id'])[2:-2] == i[2]:
                                CDS_obj = FactoryDb.CDS.get_unique(i[0], i[1], i[2], feature.location, None)
                                default_list.append(CDS_obj.ARO_Accession)
                        except KeyError:
                            pass
                        except KeyboardInterrupt:
                            break
            FactoryDb.session.commit()
        #print("CDS info added to records : ", default_list)

    def populate_prot(default_list, cds_table, card_fact_table):
        """It searches for the info of the initial and final positions of the coding sequence (CDS) of the protein within the DNA sequence, using the Protein Accession number.
        It first checks whether the info is already in the table 'cds_table'. """

        parsed_entries = QueriesFromDb.return_query_as_list(
            QueriesFromDb.select_query('ARO_Accession, DNA_Accession, Protein_Accession', cds_table))
        to_be_parsed_entries = QueriesFromDb.return_query_as_list(
            QueriesFromDb.select_query('ARO_Accession, DNA_Accession, Protein_Accession', card_fact_table))
        to_be_parsed_entries_clean = QueriesFromDb.find_not_parsed_files_general(to_be_parsed_entries, parsed_entries)
        print("Pending entries: ", to_be_parsed_entries_clean)
        for i in to_be_parsed_entries_clean:
            print("Checking: ", i)
            handle = Entrez.efetch(db='protein', id=i[2], rettype='gp', retmode='text')
            for record in SeqIO.parse(handle, 'genbank'):
                for feature in record.features:
                    if feature.type == 'CDS':
                        if record.id == i[2]:
                            try:
                                prot_obj = FactoryDb.CDS.get_unique(i[0], i[1], i[2], None, str(feature.qualifiers['coded_by'])[2:-2])
                                default_list.append(prot_obj.ARO_Accession)
                            except KeyboardInterrupt:
                                break
            FactoryDb.session.commit()
        #print("Prot info added to records : ", default_list)

    def populate_delimiters_table(fasta_table, cds_table):
        """Define the DNA basepairs comprising the coding sequence and introduce them in their table using ARO_Accession as the primary key."""
        delimiters_df = pd.read_sql_query(
            f"SELECT {cds_table}.ARO_Accession, {cds_table}.DNA_Accession, {cds_table}.Location_DNA, {cds_table}.Location_Prot, LENGTH({fasta_table}.DNA_Sequence) AS Length_DNA_Sequence FROM {cds_table} INNER JOIN {fasta_table} ON {cds_table}.DNA_Accession = {fasta_table}.DNA_Accession",
            FactoryDb.engine)
        delimiters_df['Strand'], delimiters_df['Delimiter_initial'], delimiters_df['Delimiter_final'], delimiters_df[
            'Extra_info'] = '', '', '', ''
        for row in delimiters_df.index:
            if delimiters_df['Location_DNA'][row] is not None:
                delimiters_df['Delimiter_initial'][row] = int(
                    ''.join(c for c in delimiters_df['Location_DNA'][row].split(':')[0] if c.isdigit()))
                delimiters_df['Delimiter_final'][row] = int(
                    ''.join(c for c in delimiters_df['Location_DNA'][row].split(':')[1] if c.isdigit()))
                delimiters_df['Strand'][row] = '+'
                delimiters_df['Extra_info'][row] = 'Seq from DNA_Accession info, strand +'
                if delimiters_df['Location_DNA'][row].endswith('(-)'):
                    delimiters_df['Strand'][row] = '-'
                    delimiters_df['Delimiter_initial'][row], delimiters_df['Delimiter_final'][row] = \
                        delimiters_df['Length_DNA_Sequence'][row] - delimiters_df['Delimiter_final'][row], \
                        delimiters_df['Length_DNA_Sequence'][row] - delimiters_df['Delimiter_initial'][row]
                    delimiters_df['Extra_info'][row] = 'Seq from DNA_Accession info, strand -'
            elif delimiters_df['Location_DNA'][row] is None and delimiters_df['Location_Prot'][row] is not None:
                delimiters_df['Delimiter_initial'][row] = delimiters_df['Location_Prot'][row].split(':')[1].split('..')[0]
                delimiters_df['Delimiter_final'][row] = delimiters_df['Location_Prot'][row].split(':')[1].split('..')[1]
                delimiters_df['Delimiter_initial'][row] = int(
                    ''.join(c for c in delimiters_df['Delimiter_initial'][row] if c.isdigit())) - 1
                delimiters_df['Delimiter_final'][row] = int(
                    ''.join(c for c in delimiters_df['Delimiter_final'][row] if c.isdigit()))
                delimiters_df['Strand'][row] = '+'
                delimiters_df['Extra_info'][row] = 'Seq from DNA_Prot info, strand +'
                if delimiters_df['Location_Prot'][row].startswith('complement'):
                    delimiters_df['Strand'][row] = '-'
                    delimiters_df['Delimiter_initial'][row], delimiters_df['Delimiter_final'][row] = \
                        delimiters_df['Length_DNA_Sequence'][row] - delimiters_df['Delimiter_final'][row], \
                        delimiters_df['Length_DNA_Sequence'][row] - delimiters_df['Delimiter_initial'][row]
                    delimiters_df['Extra_info'][row] = 'Seq from DNA_Prot info, strand -'
            
            obj = FactoryDb.Delimiters(delimiters_df['ARO_Accession'][row], delimiters_df['DNA_Accession'][row], delimiters_df['Strand'][row], delimiters_df['Delimiter_initial'][row], delimiters_df['Delimiter_final'][row], delimiters_df['Extra_info'][row])
            FactoryDb.session.add(obj)
            FactoryDb.session.commit()
        return delimiters_df


    def determine_CDS_sequence(fasta_table, delimiters_df):
        """Merges dataframes containing the delimiters info and the whole fasta sequences, with the objective of obtaining the coding sequence for each ARO_Accession number."""
        fasta_df = QueriesFromDb.select_query('DNA_Accession, DNA_Sequence', fasta_table)
        CDS_sequence_df = delimiters_df.merge(fasta_df, on='DNA_Accession', how='left')
        CDS_sequence_df['CDS_Sequence'] = ''
        for row in CDS_sequence_df.index:
            CDS_sequence_df['DNA_Sequence'][row] = Seq(str(CDS_sequence_df['DNA_Sequence'][row])[2:-1])
            if CDS_sequence_df['Strand'][row] == '+':
                CDS_sequence_df['CDS_Sequence'][row] = CDS_sequence_df['DNA_Sequence'][row][
                                                       int(CDS_sequence_df['Delimiter_initial'][row]):int(
                                                           CDS_sequence_df['Delimiter_final'][row])]
            elif CDS_sequence_df['Strand'][row] == '-':
                CDS_sequence_df['CDS_Sequence'][row] = CDS_sequence_df['DNA_Sequence'][row].reverse_complement()[int(CDS_sequence_df['Delimiter_initial'][row]):int(CDS_sequence_df['Delimiter_final'][row])]
        return CDS_sequence_df