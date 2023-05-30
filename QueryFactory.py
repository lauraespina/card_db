
class QueryFactory:
    def output_files(work_folder, gb_files_folder, prot_files_folder, fasta_files_folder, query_gbfasta, query_dna_2, query_prot_1, query_prot_2, query_fasta_2, list_of_objects, chunksize = 20):
        """Creates chunks of a default size of 20 DNA accession numbers of protein accession numbers in text files
        so that they can be later queried via Eutils efetch. DNA accession numbers will be queried as Genbank and Fasta format."""
        i = 0
        global txtlist
        txtlist = []
        while i <=(len(list_of_objects)-chunksize):
            chunk_dnas = []
            chunk_prots = []
            for i in range(i, i + chunksize):
                chunk_dnas.append(list_of_objects[i].DNA_Accession)
                chunk_prots.append(list_of_objects[i].Protein_Accession)
                i += 1
            f = open(work_folder + gb_files_folder + '/%d.txt' % (i-chunksize), 'w')
            print(*query_gbfasta + ','.join(map(str, chunk_dnas)) + query_dna_2, file=f, sep="")
            f = open(work_folder + prot_files_folder + '/%d.txt' % (i - chunksize), 'w')
            print(*query_prot_1 + ','.join(map(str, chunk_prots)) + query_prot_2, file=f, sep="")
            f = open(work_folder + fasta_files_folder + '/%d.txt' % (i-chunksize), 'w')
            print(*query_gbfasta + ','.join(map(str, chunk_dnas)) + query_fasta_2, file=f, sep="")

            # Create the list of text files
            title = '%d.txt' % (i-chunksize)
            txtlist.append(title)
        i += chunksize
        # Create the query for the last <20 accession numbers
        chunk_dnas = [list_of_objects[j].DNA_Accession for j in range((i-chunksize), len(list_of_objects))]
        chunk_prots = [list_of_objects[j].Protein_Accession for j in range((i - chunksize), len(list_of_objects))]
        f = open(work_folder + gb_files_folder + str(i-chunksize) + '.txt', 'w')
        print(*query_gbfasta + ','.join(map(str, chunk_dnas)) + query_dna_2, file=f, sep="")
        f = open(work_folder + prot_files_folder + str(i-chunksize) + '.txt', "w")
        print(*query_prot_1 + ','.join(map(str, chunk_prots)) + query_prot_2, file=f, sep="")
        f = open(work_folder + fasta_files_folder + str(i - chunksize) + '.txt', "w")
        print(*query_gbfasta + ','.join(map(str, chunk_dnas)) + query_fasta_2, file=f, sep="")
        # Add the last file to the text list
        txtlist.append(str(i-chunksize)+'.txt')
        return txtlist