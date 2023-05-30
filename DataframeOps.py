import pandas as pd

class DataframeOps:

    def read_data(work_folder, filename):
        """ Takes the relevant info from the aro_index.tsv file found within the list of files to create our table. """
        dataframe = pd.read_table(work_folder + filename, keep_default_na= False)
        dataframe.columns = dataframe.columns.str.replace(' ', '_')
        return dataframe

    def export_excel(work_folder, dataframe, excelfile):
        """ Exports the dataframe as an excel file. """
        dataframe.to_excel(work_folder + excelfile, index = None)

    def export_csv(work_folder, dataframe, tsvfile):
        """ Exports the dataframe as a csv file. """
        dataframe.to_csv(work_folder + tsvfile, sep = '\t', index = None)
