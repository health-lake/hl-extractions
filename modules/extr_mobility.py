from logging import exception
import requests
import boto3
from datetime import date
import os
from utils.chrome_driver import ChromeDriver
from utils.s3_writer_operator import HandlerS3Writer


# Armazenando as keys.
#AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
#AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

FILE_NAME = 'global_mobility.csv'
URL = 'https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv'
DATA_ATUAL = date.today()

class ExtractMOBILITY:

    print("Inicio da extração dos dados de mobilidade.")

    # def __init__(self):
    #     self.url="https://www.google.com/covid19/mobility/"
    #     self.driver=ChromeDriver.get_driver(self.url)

    def download(self):

        try:
            # Request no arquivo alvo para download.
            print("Baixando: {}".format(FILE_NAME)) 
            r = requests.get(URL, stream=True, allow_redirects=True)
        except Exception as e:
            print('REQUEST ERROR')  
            print('Error: {e}')  

        try:
            # Grava arquivo no bucket S3
            s3_writer = HandlerS3Writer(
                extracted_file=r.content,
                extraction_name=FILE_NAME,
                extraction_source=f'mobility/{DATA_ATUAL}' 
            )
        except Exception as e:
            print('UPLOAD ERROR')
            print('Error: {e}')

        print("Fim da coleta dos dados da mobilidade.") 