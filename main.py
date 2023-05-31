"""This is the main script for v. 1.0, which executes the following steps:
    - Declarative mapping of all the defined classes
    - Population of the relational databases from original file and from requests via Eutils
    - Load of all the information onto the relational database
    - Export of the most relevant information in worksheet format 
"""
from FileManagement import FileManagement
from PopulateDb import PopulateDb
from QueriesFromDb import QueriesFromDb
from UpdateDb import UpdateDb
import FactoryDb

from personal_info import work_folder, email
from Bio import Entrez
import pandas as pd
import sqlalchemy


pd.options.mode.chained_assignment = None

# Variables
# ------------------------------------------------
origin_file = 'aro_index.tsv'
card_origin_filename = 'cardfile.tar.bz2'
card_url = 'https://card.mcmaster.ca/download/0/broadstreet-v3.2.5.tar.bz2'
default_list = []


# Create a database schema with the name 'card_db' and update email details for Eutils 
Entrez.email = email

# Download the CARD origin file'

FileManagement.download_cardfile(card_origin_filename, work_folder, card_url)

# Create first table 'card_fact_table':
list_of_card_objects = PopulateDb.populate_ARO(work_folder, origin_file, default_list)

# Examine the entries parsed to the card_fact_table:
QueriesFromDb.find_not_parsed_files_first_table('card_fact_table', work_folder, origin_file)
duplicates = QueriesFromDb.find_duplicates(QueriesFromDb.entries_to_be_parsed_from_original_file(work_folder, origin_file)[0])
print("List of ARO_Accession numbers that appear as duplicates in the original file: ", duplicates, " Check whether they are coincident with the Entries in original file which have not been parsed to the database.")

# Create second table 'fasta_table'.
PopulateDb.populate_FASTA(default_list, 'fasta_table', 'card_fact_table')

# Create third table 'cds_table'.
PopulateDb.populate_CDS(default_list, 'cds_table', 'card_fact_table')
PopulateDb.populate_prot(default_list, 'cds_table', 'card_fact_table')

# Define the basepairs limiting the coding sequence for each entry and create a table to store them:
delimiters_df = PopulateDb.populate_delimiters_table('fasta_table', 'cds_table')

# Extract the coding sequences for each entry:
CDS_sequence_df = PopulateDb.determine_CDS_sequence('fasta_table', delimiters_df)

# Update the card_fact_table with the coding sequences and the extra info:
dict_cdsseq = {CDS_sequence_df['ARO_Accession'][row]:CDS_sequence_df['CDS_Sequence'][row] for row in CDS_sequence_df.index}
dict_extrainfo = {CDS_sequence_df['ARO_Accession'][row]:CDS_sequence_df['Extra_info'][row] for row in CDS_sequence_df.index}
UpdateDb.create_column('card_fact_table', 'CDS_Sequence', 'VARCHAR(9000)')
UpdateDb.create_column('card_fact_table', 'Extra_info', 'VARCHAR(255)')
UpdateDb.update_column('card_fact_table', dict_cdsseq, 'CDS_Sequence')
UpdateDb.update_column('card_fact_table', dict_extrainfo, 'Extra_info')

# Update the Extra_info of the empty entries specifying that the whole DNA sequence must be used:
extrainfotable = sqlalchemy.Table('card_fact_table', sqlalchemy.MetaData(bind=FactoryDb.engine), autoload=True)
FactoryDb.engine.execute(sqlalchemy.update(extrainfotable).where(extrainfotable.c.CDS_Sequence == None).values({extrainfotable.c.Extra_info: 'Whole DNA Sequence'}))

# All the tables are in MySQL now. Finally, export the whole table as an excel file if needed.
whole_table = pd.read_sql_table('card_fact_table', FactoryDb.engine)
whole_table.to_excel("final_table.xlsx")
