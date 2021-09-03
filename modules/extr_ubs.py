from modules.extr_dgbr import DGBRXtractor


class ExtractUBS:
    def __init__(self):
        self.target_url = "hhttps://dados.gov.br/dataset/unidades-basicas-de-saude-ubs"
        self.extensions = [".csv"]

    def download(self):
        xtr = DGBRXtractor("UBS")
        xtr.get_files_by_ds_url(self.target_url, ext=self.extensions)