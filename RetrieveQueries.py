import os
import requests


class RetrieveQueries:

    def query_fasta(work_folder, fasta_files_folder, txtlist):
        """ Queries the dna txt files created before for the content in fasta format. Requires internet connection."""
        for file in os.listdir(work_folder + fasta_files_folder):
            if file in txtlist:
                file_path = f"{work_folder + fasta_files_folder}{file}"
                with open(file_path) as f:
                    lines = f.readlines()
                    page = requests.get(lines[0])
                    x = open(work_folder + fasta_files_folder + str(file[:-4]) + '.fasta', 'w')
                    x.write(page.text)

    def query_dna(work_folder, gb_files_folder, txtlist):
        """ Queries the dna txt files created before for the content in genbank format. Requires internet connection."""
        for file in os.listdir(work_folder + gb_files_folder):
            if file in txtlist:
                file_path = f"{work_folder + gb_files_folder}{file}"
                with open(file_path) as f:
                    lines = f.readlines()
                    page = requests.get(lines[0])
                    x = open(work_folder + gb_files_folder + str(file[:-4]) + '.gb', 'w')
                    x.write(page.text)

    def query_prot(work_folder, prot_files_folder, txtlist):
        """ Queries the prot txt files created before for the content in genbank-prot format. Requires internet connection."""
        for file in os.listdir(work_folder + prot_files_folder):
            if file in txtlist:
                file_path = f"{work_folder + prot_files_folder}{file}"
                with open(file_path) as f:
                    lines = f.readlines()
                    page = requests.get(lines[0])
                    x = open(work_folder + prot_files_folder + str(file[:-4]) + '.gp', 'w')
                    x.write(page.text)