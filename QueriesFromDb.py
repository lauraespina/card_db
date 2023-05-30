import FactoryDb
import pandas as pd
import csv
import collections

class QueriesFromDb():
    def select_query(columns, table):
        """Launch SQL statement 'Select column from table and return a list containing all elements of the list'."""
        query = pd.read_sql_query(f"SELECT {columns} FROM {table}", FactoryDb.engine)
        return query

    def return_query_as_list(query):
        """Returns the dataframe from a query of a single-column or two-columns selection as a list."""
        list_of_columns = [column for column in query.columns.values]
        if len(query.columns.values) == 1:
            returned_query = list((query[f"{list_of_columns[0]}"]))
        if len(query.columns.values) == 2:
            returned_query = list(zip(list(query[f"{query.columns.values[0]}"]), list(query[f"{query.columns.values[1]}"])))
        if len(query.columns.values) == 3:
            returned_query = list(zip(list(query[f"{query.columns.values[0]}"]), list(query[f"{query.columns.values[1]}"]), list(query[f"{query.columns.values[2]}"])))
        return returned_query

    def entries_to_be_parsed_from_original_file(work_folder, origin_file):
        """Identifies the entries to be parsed to the table 'card_fact_table' from the tsv file by identifying each entry through the ARO_Accession
         and the Model_ID numbers. Returns a list of the entries identified by these IDs plus another list with their DNA_Accession and Protein_Accession numbers. """
        to_be_parsed_entries, to_be_parsed_entries_metadata = [], []
        with open(work_folder + origin_file) as tsv_aro:
            rd = csv.reader(tsv_aro, delimiter='\t')
            next(rd)
            for row in rd:
                to_be_parsed_entries += [(row[0], row[3])]
                to_be_parsed_entries_metadata += [(row[7], row[6])]
        return to_be_parsed_entries, to_be_parsed_entries_metadata

    def find_duplicates(list_of_entries):
        """Finds duplicate entries in a list of files to be parsed."""
        if any(isinstance(i, list) for i in list_of_entries) == False:
            list_expression = [i[0] for i in list_of_entries]
        if any(isinstance(i, list) for i in list_of_entries) == True:
            list_expression = [i[0] for i in list_of_entries]
        duplicates = [item for item, count in collections.Counter(list_expression).items() if count > 1]
        return duplicates

    def find_not_parsed_files_general(to_be_parsed_entries, parsed_entries):
        for i in sorted(to_be_parsed_entries):
            if i in sorted(parsed_entries):
                to_be_parsed_entries.remove(i)
        return to_be_parsed_entries

    def find_not_parsed_files_first_table(tablename, work_folder, origin_file):
        parsed_entries = QueriesFromDb.return_query_as_list(QueriesFromDb.select_query('ARO_Accession, Model_ID', tablename))
        to_be_parsed_entries, to_be_parsed_entries_metadata = QueriesFromDb.entries_to_be_parsed_from_original_file(work_folder, origin_file)
        to_be_parsed_entries_cleaned = QueriesFromDb.find_not_parsed_files_general(to_be_parsed_entries, parsed_entries)
        print("Entries in original file which have not been parsed to the database: ", to_be_parsed_entries_cleaned)
        print("DNA_Accession numbers and Protein_Accession numbers associated with the entries which have not been parsed to the database: ",
            ([to_be_parsed_entries_metadata[to_be_parsed_entries.index(i)] for i in to_be_parsed_entries_cleaned]))
