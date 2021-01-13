# -*- coding: utf-8 -*-

from tools.DGBRXtractor import DGBRXtractor

class ExtractSRAG:

    def __init__(self):
        self.target_url = 'https://dados.gov.br/dataset/bd-srag-2020'
        self.extensions = ['.csv']
    
    def download(self):
        xtr = DGBRXtractor()
        xtr.get_files_by_ds_url(self.target_url, ext=self.extensions)