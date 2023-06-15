import os
import json
import pymongo

from personal_info import Mongo, work_folder
from FileManagement import FileManagement

card_origin_filename = 'cardfile.tar.bz2'
card_url = 'https://card.mcmaster.ca/download/0/broadstreet-v3.2.5.tar.bz2'
original_json = work_folder+'card.json'
correct_json = work_folder+'correct_json.json'

client = Mongo.client
db = Mongo.db
collection = Mongo.collection
requesting = []

def make_json_parsable(original_json, correct_json):
    """The original card.json file is not correctly formatted to be directly parsed into MongoDB, this function fixes this."""
    file_original_json = open(original_json, 'r')
    data_original_json = json.loads(file_original_json.read())
    if isinstance(data_original_json, dict) and 'model_id' not in data_original_json.keys():
        data_correct_json = [v for k, v in data_original_json.items() if isinstance(v, dict) and 'model_id' in list(v.keys())] 
    elif isinstance(data_original_json, list) and 'model_id' in data_original_json[0].keys():
        data_correct_json = data_original_json
    elif isinstance(data_original_json, dict) and 'model_id' in list(data_original_json.keys()):
        data_correct_json = data_original_json
    json.dump(data_correct_json, open(correct_json, 'w'))

def truncate_json(correct_json):
    """The original card.json file is too big to be parsed into MongoDB, this function fixes this."""
    file_json = open(correct_json, 'r')
    data_json = json.loads(file_json.read())
    sizefile = os.path.getsize(correct_json)
    if isinstance(data_json, list) and sizefile/16000000 > 1:
        chunks = (round(sizefile/16000000) + 1)
        n = int(len(data_json)/chunks)
        number_file = 1
        for i in range(0, len(data_json), n):
            f = work_folder + 'correct_json_%d.json' % number_file
            json.dump(data_json[i: i+n], open(f, 'w'))
            number_file += 1
        file_json.close()
        os.remove(correct_json)


def populate_mongodb(work_folder):
    """Creates a list of entries to be loaded into MongoDB, from the json file(s). """
    for file in os.listdir(work_folder):
        if file.endswith('.json') and file.startswith('correct_json'):
            with open(file) as f:
                content = json.loads(f.read())
                if isinstance(content,list):
                    for jsonObj in content:
                        requesting.append(pymongo.InsertOne(jsonObj))
                elif isinstance(content, dict):
                    requesting.append(pymongo.InsertOne(content))
    return requesting


FileManagement.download_cardfile(card_origin_filename, work_folder, card_url)

make_json_parsable(original_json, correct_json)
truncate_json(correct_json)
requesting = populate_mongodb(work_folder)

result = collection.bulk_write(requesting)
client.close()