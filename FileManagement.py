import requests
import shutil

class FileManagement:

    def download_cardfile(card_origin_filename, work_folder, card_url):
        """ Downloads the CARD dataset and unpacks the files """
        try:
            card_get = requests.get(card_url, allow_redirects=True)
            with open(work_folder + card_origin_filename, 'wb') as f:
                f.write(card_get.content)
                shutil.unpack_archive(work_folder + card_origin_filename, work_folder)
        except:
            print('Check internet connection and URL address.')
