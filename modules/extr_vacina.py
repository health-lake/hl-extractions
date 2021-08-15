import requests
import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from datetime import date
import datetime

from utils.s3_writer_operator import HandlerS3Writer

# Instalar a engine fastparquet caso use parquet (pip install fastparquet)


# Configurar aqui antes de rodar
endereco_api = "https://imunizacao-es.saude.gov.br/_search"
user = "imunizacao_public"
password = "qlto5t&7r_@+#Tlstigi" 
generated_filename = "consolidado_vacinas_sus"

class ExtractVACINA:

    def upload_to_aws(self, local_file, bucket, s3_file):
        s3 = boto3.client('s3')
        s3.upload_file(local_file, bucket, s3_file)


    ############### Functions ###############
    def upload_file_s3(self, file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            print(e)
            return False
        return True

    ############### MAIN CODE ###############
    # # Primeira request
    ## FULLLOAD
    ## Para gerar o fullload é necessário  remover a função lambda_handler
    ## pois ela é necessária apenas no código lambda

    def download(self):
        today = date.today()
        day = datetime.timedelta(1)
        today = today - day
        vacina = f"{today.year}-{today.month:02d}-{today.day:02d}T00:00:00.000Z"
        
        #vacina = "2021-07-09T15:55:20.019Z"

        ## FULLLOAD
        ## Para gerar o fullload é necessário remover a chave query do dicionário.
        try:
            data= {
            "size": 10000
            ,
            "query": {
                "bool": {
                "filter": [
                    { "term": { "vacina_dataAplicacao" : f"{today.year}-{today.month:02d}-{today.day}T00:00:00.000Z"}}
                ]
                }
            }
            }
            vacinas_raw = requests.get(
                endereco_api + "?scroll=1m", 
                headers={"Content-Type": "application/json"}, 
                auth=(user, password), 
                data=json.dumps(data)
            ).text
            dados_vacina = json.loads(vacinas_raw)
        except Exception as ex:
            print("Erro na requisicao/parsing dos dados da API em" + endereco_api + ". Erro:" +  ex)

        current_page = 1
        print("Requested page " + str(current_page))


        # Navega nas paginas ate acabar
        while True:
            # Se retornar erro
            if "error" in dados_vacina:
                print("Erro nos dados da vacina")
                print(dados_vacina["error"])
                raise Exception("Error found on request result")
            
            # Se retornar timeout
            if dados_vacina["timed_out"] == True:
                print("Request result returned timeout status")
                raise Exception("Request timed out in the API server")

            # Pagina vazia, ou seja, acabaram os dados
            if dados_vacina["hits"]["hits"] == None or len(dados_vacina["hits"]["hits"]) == 0:
                print("Página vazia")
                break
                
            # Pega apenas a parte relevante dos dados para guardar
            dados_limpos = [entry["_source"] for entry in dados_vacina["hits"]["hits"]]
            
            # Escreve um arquivo por pagina
            with open('/tmp/' + generated_filename + '_' + str(current_page) + '.json', "w") as f:
                json.dump(dados_limpos, f)
            
            page_id = dados_vacina["_scroll_id"]

            if not page_id:
                break
            
            data= {
            "scroll": "30m",
            "scroll_id": page_id
            }
            try:
                vacinas_raw = requests.post(
                    endereco_api + "/scroll", 
                    headers={"Content-Type": "application/json"}, 
                    auth=(user, password), 
                    data=json.dumps(data)
                ).text
                dados_vacina = json.loads(vacinas_raw)
            except Exception as ex:
                print("Erro na requisicao/parsing dos dados da API em" + endereco_api + "com scroll id" + page_id + ". Erro: " + ex)
            

            
            #self.upload_to_aws(
            #    '/tmp/' + generated_filename + '_' + str(current_page) + '.json','covid-lake-data',
            #    'raw/vacina/' + today.strftime("%Y/%m/%d/") + generated_filename + '_' + str(current_page) + '.json')
            
            # Grava no S3
            s3_writer = HandlerS3Writer(
                extracted_file=f"/tmp/{generated_filename}_{str(current_page)}.json",
                extraction_name=f"{generated_filename}_{str(current_page)}.json'",
                extraction_source="vacina",
                bucket='covid-lake-data'
            )

            current_page += 1
            print("Requested page " +  str(current_page))
