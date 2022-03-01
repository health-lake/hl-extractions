from logging import exception
import requests
from datetime import date
from utils.s3_writer_operator import HandlerS3Writer

# CRIAÇÃO DE VARIÁVEIS
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
            # REQUEST NO LINK DO ARQUIVO A SER BAIXADO
            print("Baixando: {}".format(FILE_NAME)) 
            r = requests.get(URL, stream=True, allow_redirects=True)
        except Exception as e:
            print('REQUEST ERROR')  
            print('Error: {e}')  

        try:
            # GRAVANDO NO BUCKET S3
            s3_writer = HandlerS3Writer(
                extracted_file=r.content,
                extraction_name=FILE_NAME,
                extraction_source=f'mobility' 
            )
        except Exception as e:
            print('UPLOAD ERROR')
            print('Error: {e}')

        print("Fim da coleta dos dados da mobilidade.") 