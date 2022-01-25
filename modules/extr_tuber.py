from logging import exception
import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import utils.s3_writer_operator
import boto3
import sys
from datetime import datetime
import os
#from utils.chrome_driver import ChromeDriver
#from utils.s3_writer_operator import HandlerS3Writer
#from modules.extr_dgbr import c



class Extract_Tuberculose:
    def __init__(self):
        self.url="https://datasus.saude.gov.br/acesso-a-informacao/casos-de-tuberculose-desde-2001-sinan/"
        self.driver=webdriver.Chrome()
        #self.extensions = [".csv"]
        
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
            print("Espera 1")
            time.sleep(2)

            #CLICA CAIXA DE SELECAO
            self.driver.find_element_by_xpath("//*[@id='mySelect']").click()
            print("Espera 2")
            time.sleep(2)

            #ESCOLHE ESTADO
            i=i.lower()
            print('o arquivo é  :: http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sinannet/cnv/tuberc{i}.def')
            action.key_down(Keys.CONTROL).click(select_estados.select_by_value(
                f' http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sinannet/cnv/tuberc{i}.def')) \
             .key_up(Keys.CONTROL).perform()
            #self.driver.find_element_by_xpath(f"/html/body/div[1]/div/div/section[3]/div/div/div[2]/div/div/div/div/div/select/option[{i}}]").click()
            
            print("Seleciona linha ano-diagnotico")
            time.sleep(2)
            
            #Seleciona 'ANO DIAGNOSTICO
            self.driver.find_element_by_xpath('/html/body/div/div/center/div/form/div[2]/div/div[1]/select/option[1]').click()
            print("Seleciona faixa etaria")
            time.sleep(2)
            #Seleciona coluna 'Faixa etaria'
            self.driver.find_element_by_xpath('/html/body/div/div/center/div/form/div[2]/div/div[2]/select/option[19]').click()
            print("Seleciona anos")
            time.sleep(2)

            #SELECIONA ANOS
            action = ActionChains(self.driver)
            
            # create select for action
            select_tipo = Select(self.driver.find_element_by_name('Arquivos'))

            #SELECIONA OS ANOS DE INTERESSE
            for o in (["{:02d}".format(n) for n in reversed(range(1,20))]):
                action.key_down(Keys.CONTROL).click(select_tipo.select_by_value(f'tube{i}{o}.dbf')) \
                .key_up(Keys.CONTROL).perform()

            print("Espera para clicar no botao de mostrar")
            time.sleep(2)

            #SELECIONA FAIXA ETARIA DE 1-4 ANOS
            #self.driver.find_element_by_xpath('//*[@id="fig20"]').click()
            #self.driver.find_element_by_xpath('/html/body/div[1]/div/center/div/form/div[4]/div[1]/div/div[20]/label[1]').click()
            
    
            #Separado por ;
            #self.driver.find_element_by_xpath('//*[@id="F"]').click()
        
            #Botao mostrar
            self.driver.find_element_by_xpath('/html/body/div/div/center/div/form/div[4]/div[2]/div[2]/input[1]').click()
            print("Espera pra fazer download csv")
            time.sleep(2)

            #baixar csv
            self.driver.find_element_by_xpath('/html/body/div/div/div[3]/table[1]/tbody/tr/td[1]/a').click()
            time.sleep(5)

            print("Feito o download para o pc")
            file_name=f'tuberc_fx_etaria_{i.upper()}.csv'

            #S3WriterOperator(extraction_file, file_name, extraction_source, bucket_name='health-lake-input')


            #TENTAR FAZER DOWNLOAD POR AQUI PARA GRAVAR NO S3

            elementos = self.driver.find_elements_by_partial_link_text('.CSV')
            for elem in elementos:
                url = elem.get_attribute("href")
                print(url)


                
                # Verificar se já existe uma pasta no diretório de execução com a identificação do dataset que pegamos lá em cima, caso não exista ela será criada
                dataset_id = url.split("/")[-1]
                if not os.path.exists(dataset_id):
                    os.makedirs(dataset_id)

                # Baixar o arquivo utilizando a biblioteca requests
                downloadable_url = url#.split("=")[1]
                print("Downloading {}".format(file_name))
                req = requests.get(downloadable_url)                
                
                # Grava no S3
                s3_writer = HandlerS3Writer(
                    extracted_file=req.content,
                    extraction_name=file_name,
                    extraction_source="tuberculose" #self.datasource,
                )
            




        #self.driver.close()


#        page = requests.get(source_code)
      #  soup = bs.BeautifulSoup(page.text, 'html.parser')
     #       table = soup.find_all('table', id= "dados")
        #df = pd.read_html(str(table), encoding = 'utf-8', decimal=',', thousands='.')[0]
       # print(df)

        self.driver.close()
#if __name__=="__main__":
try:
    Extract_Tuberculose().download()
except exception as e:
    print(e)
#Extract_Tuberculose()