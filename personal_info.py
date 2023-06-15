import os 
import pymongo

work_folder = str(os.path.abspath(os.getcwd()).replace(os.sep, '/')+'/')
sql_dialect_driver = 'mysql'
username = 'root'
password = ''
host = 'host'
database_name = 'card_db'
email = ''

#Only for importing onto MongoDB:

class Mongo():
    client = pymongo.MongoClient()
    db = client.Card_DB
    collection = db.card_fact_table