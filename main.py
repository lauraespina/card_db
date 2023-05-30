"""This is the main script for v. 1.0, which executes the following steps:
    - Creation of several directories and download the data from the Card database
    - Creation of Card objects from the entries of the dataset
    - Division of all entries in groups of 20 items to retrieve info from Genbank via Requests and Eutils
    - Saving info in txt files
    - Updating the Card objects with the genomic info (sequence of the coding region for each antibiotic resistance gene) from the txt files
    - Loading the parsed genomic info into a worksheet, showing the initial dataset plus the sequences of the coding regions

"""

from FileManagement import FileManagement
from DataframeOps import DataframeOps
from Card import Card
from CardList import CardList
from QueryFactory import QueryFactory
from RetrieveQueries import RetrieveQueries
from AddAttributes import AddAttributes
from personal_info import work_folder


# Variables
# -------------------

card_origin_filename = 'cardfile.tar.bz2'
card_url = 'https://card.mcmaster.ca/download/0/broadstreet-v3.2.5.tar.bz2'
gb_files_folder = 'gb_files/'
fasta_files_folder = 'fasta_files/'
card_data_output = 'card_data.xlsx'
prot_files_folder = 'prot_files/'
query_gbfasta = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id='
query_dna_2 = '&rettype=gb&retmode=text'
query_fasta_2 = '&rettype=fasta&retmode=text'
query_prot_1 = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id='
query_prot_2 = '&rettype=gp&retmode=text'
origin_file = 'aro_index.tsv'

# Variables within classes and methods
# -----------------------------------------------
    #card_df: dataframe with the info from tsv_file
    #list_of_card_objects: list containing all the DNA_Accession and Protein_Accession
    #txtlist: from 0.txt to 5020.txt


FileManagement.checkfolders(work_folder, gb_files_folder, prot_files_folder, fasta_files_folder)
FileManagement.download_cardfile(card_origin_filename, work_folder, card_url)
card_df = DataframeOps.read_data(work_folder, origin_file)
list_of_card_objects = CardList.create_list_of_objects(card_df)

DataframeOps.export_excel(work_folder, card_df, card_data_output)
txtlist = QueryFactory.output_files(work_folder, gb_files_folder, prot_files_folder, fasta_files_folder, query_gbfasta, query_dna_2, query_prot_1, query_prot_2, query_fasta_2, list_of_card_objects)
RetrieveQueries.query_fasta(work_folder, fasta_files_folder, txtlist)
RetrieveQueries.query_dna(work_folder, gb_files_folder, txtlist)
RetrieveQueries.query_prot(work_folder, prot_files_folder, txtlist)
AddAttributes.add_seqs(work_folder, fasta_files_folder, list_of_card_objects)
AddAttributes.add_dna_cds(work_folder, gb_files_folder, list_of_card_objects)
AddAttributes.add_prot_cds(work_folder, prot_files_folder, list_of_card_objects)

# If a safety copy is needed at this point:
# --------------------------------------------
# Create the dataframe from the list of objects:
#   safety_copy = CardList.create_dataframe_from_list_of_objects(list_of_card_objects)
# Export to a tsv file:
#   DataframeOps.export_csv(safety_copy, 'safety_copy.tsv')
# Read from the tsv file:
#   readsafetycopy = DataframeOps.read_data('safety_copy.tsv')
# Create the list of objects from the dataframe:
#   list_of_card_objects2 = CardList.create_list_of_objects(readsafetycopy)

# Update the DNA sequences corresponding to the ARGs
# -----------------------------------------------------------
for i in list_of_card_objects:
    Card.update_delimiters(i)
    Card.define_sequence(i)

final_dataframe = CardList.create_dataframe_from_list_of_objects(list_of_card_objects)
DataframeOps.export_excel(work_folder, final_dataframe, 'final_info.xlsx')
