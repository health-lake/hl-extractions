from logging import exception
import requests
import time
import boto3
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import utils.s3_writer_operator
import sys
from datetime import datetime
import os
from utils.chrome_driver import ChromeDriver
from utils.s3_writer_operator import HandlerS3Writer
#from modules.extr_dgbr import c



class Extract_Tuber_regiao:
    def __init__(self):
        self.url="https://datasus.saude.gov.br/acesso-a-informacao/casos-de-tuberculose-desde-2001-sinan/"
        #self.driver=webdriver.Chrome()
        self.driver=ChromeDriver.get_driver(self.url)


    def download(self):


        estados=["AL","AC","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG",\
            "PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]
        print(estados[0].lower)

        for i in estados:
            self.driver.get(self.url)
            self.driver.implicitly_wait(2)
            time.sleep(2)

            #ACTION PARA SELECAO DE ESTADOS    
            action = ActionChains(self.driver)
                    # # create select for action
            select_estados = Select(self.driver.find_element_by_id('mySelect'))
            #CLICA RADIO BUTTON
            self.driver.find_element_by_xpath("/html/body/div[1]/div/div/section[3]/div/div/div[2]/div/div/div/div/div/div[1]/input").click()



            #CLICA CAIXA DE SELECAO
            self.driver.find_element_by_xpath("//*[@id='mySelect']").click()            


            #ESCOLHE ESTADO
            i=i.lower()
            estado=i.upper()
            print('o arquivo é  :: http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sinannet/cnv/tuberc{i}.def')
            action.key_down(Keys.CONTROL).click(select_estados.select_by_value(
                f' http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sinannet/cnv/tuberc{i}.def')) \
             .key_up(Keys.CONTROL).perform()
            #self.driver.find_element_by_xpath(f"/html/body/div[1]/div/div/section[3]/div/div/div[2]/div/div/div/div/div/select/option[{i}}]").click()


            loop=-1
            #SELECIONA OS ANOS DE INTERESSE
            for o in (["{:02d}".format(n) for n in reversed(range(1,21))]):
                loop=loop+1

                print(f'Estado {str(i.upper)} e ano de 20{str(o)}')
                print("Seleciona regiao do estado como linha da tabela")


                #Seleciona linha como 'REGIAO do ESTADO'
                self.driver.find_element_by_xpath('/html/body/div/div/center/div/form/div[2]/div/div[1]/select/option[8]').click()
                #/html/body/div/div/center/div/form/div[2]/div/div[1]/select/option[8]
                print("Seleciona faixa etaria como coluna da tabela")


                #Seleciona coluna 'Faixa etaria'
                self.driver.find_element_by_xpath('/html/body/div/div/center/div/form/div[2]/div/div[2]/select/option[19]').click()
                #escolaridade:                     /html/body/div/div/center/div/form/div[2]/div/div[2]/select/option[22]
                #raca                               /html/body/div/div/center/div/form/div[2]/div/div[2]/select/option[23]
                #linha região 
                #print("Seleciona ano")


                #SELECIONA ANOS
                select_tipo = Select(self.driver.find_element_by_name('Arquivos'))
                if loop>0:select_tipo.deselect_by_value(f'tube{i}20.dbf')
                select_tipo.select_by_value(f'tube{i}{o}.dbf')

                #Botao mostrar
                self.driver.find_element_by_xpath('/html/body/div/div/center/div/form/div[4]/div[2]/div[2]/input[1]').click()
                print("Sobe tabela pro S3")

                #self.driver.find_element_by_xpath('/html/body/div/div/div[3]/table[1]/tbody/tr/td[1]/a').click()
                time.sleep(1)

                file_name=f'regiao_fx_etaria_20{o}_{i.upper()}.csv'

                #GRAVAR NO S3

                elementos = self.driver.find_elements_by_partial_link_text('.CSV')
                for elem in elementos:
                    url = elem.get_attribute("href")
                    print(url)


                    # Verificar se já existe uma pasta no diretório de execução com a identificação do dataset que pegamos lá em cima, caso não exista ela será criada
                    dataset_id = url.split("/")[-1]
                    if not os.path.exists(dataset_id):
                        os.makedirs(dataset_id)

                    try:
                        # Baixar o arquivo utilizando a biblioteca requests
                        downloadable_url = url#.split("=")[1]
                        print("Downloading {}".format(file_name))
                    # req = requests.get(downloadable_url)    
                        req=requests.get(url, stream=True, allow_redirects=True,#)
                        headers={'user-agent': 'MyPC'})
                    except Exception as e:
                        print('Erro no get.request')  
                        print(e)  

                    try:
                        # Grava no S3
                        s3_writer = HandlerS3Writer(
                            extracted_file=req.content,
                            extraction_name=file_name,
                            extraction_source=f'tuberculose/{estado}' #self.datasource,
                        )
                    except Exception as e:
                        print('Erro ao transferir arquivo para s3')
                        print('O erro é {e}')

                #CLICA NO BOTAO VOLTAR
                self.driver.find_element_by_xpath('/html/body/div/div/div[3]/table[2]/tbody/tr/td/a').click()


        self.driver.close()
#if __name__=="__main__":
try:
    Extract_Tuber_regiao().download()
except exception as e:
    print(e)
#Extract_Tuberculose()