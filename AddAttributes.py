import os
from Bio import SeqIO

class AddAttributes:

    def add_seqs(work_folder, fasta_files_folder, list_of_objects):
        """Update the list of objects with the attribute of the DNA sequence."""
        for file in os.listdir(work_folder + fasta_files_folder):
            if file.endswith('.fasta'):
                file_path = f"{work_folder + fasta_files_folder}{file}"
                for record in SeqIO.parse(file_path, 'fasta'):
                    for i in list_of_objects:
                        if record.id == i.DNA_Accession:
                            i.DNA_Sequence = record.seq

    def add_dna_cds(work_folder, gb_files_folder, list_of_objects):
        """Update the list of objects with the attribute of the CDS info from the Genbank file."""
        for file in os.listdir(work_folder + gb_files_folder):
            if file.endswith('.gb'):
                file_path = f"{work_folder + gb_files_folder}{file}"
                for record in SeqIO.parse(file_path, 'genbank'):
                    for i in list_of_objects:
                        if record.id == i.DNA_Accession:
                            for feature in record.features:
                                if feature.type == 'CDS':
                                    try:
                                        if str(feature.qualifiers['protein_id'])[2:-2] == i.Protein_Accession:
                                            i.DNA_CDS = str(feature.location)
                                    except KeyError:
                                        pass

    def add_prot_cds(work_folder, prot_files_folder, list_of_objects):
        """Update the list of objects with the attribute of the CDS info from the protein file."""
        for file in os.listdir(work_folder + prot_files_folder):
            if file.endswith('.gp'):
                file_path = f"{work_folder + prot_files_folder}{file}"
                for record in SeqIO.parse(file_path, 'genbank'):
                    for feature in record.features:
                        if feature.type == 'CDS':
                            for i in list_of_objects:
                                if i.Protein_Accession == record.id:
                                    i.prot_CDS = str(feature.qualifiers['coded_by'])[2:-2]
