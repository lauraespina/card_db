import os
import requests
import shutil

class FileManagement:

    def checkfolders(work_folder, gb_folder, prot_folder, fasta_folder):
        """ Create two folders, one for DNA files and another for protein files, """
        try:
            if not os.path.exists(work_folder + gb_folder):
                os.makedirs(work_folder + gb_folder)
            if not os.path.exists(work_folder + prot_folder):
                os.makedirs(work_folder + prot_folder)
            if not os.path.exists(work_folder + fasta_folder):
                os.makedirs(work_folder + fasta_folder)
        except:
            print('Folders not created. Try again.')


    def download_cardfile(card_origin_filename, work_folder, card_url):
        """ Downloads the CARD dataset and unpacks the files """
        try:
            card_get = requests.get(card_url, allow_redirects=True)
            with open(work_folder + card_origin_filename, 'wb') as f:
                f.write(card_get.content)
                shutil.unpack_archive(work_folder + card_origin_filename, work_folder)
        except:
            print('Check internet connection and URL address.')