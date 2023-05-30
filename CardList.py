import pandas as pd
from Card import Card

class CardList:
    def create_list_of_objects(dataframe):
        """Automatically creates a list of objects containing the info on the dataframe from the aro_index.tsv file, or any other dataframe.
        The key attributes have been specified in the class, but dynamic instantiating allows us to maintain the rest of attributes. """
        list_of_objects = []
        for each_record in dataframe.index:
            obj = Card()
            for column in dataframe.columns:
                setattr(obj, column, dataframe[column][each_record])
            list_of_objects.append(obj)
        return list_of_objects

    def create_dataframe_from_list_of_objects(list_of_objects):
        dataframe = pd.DataFrame([[v for k, v in vars(i).items()] for i in list_of_objects])
        dataframe.columns = [k for k, v in vars(list_of_objects[0]).items()]
        return dataframe
