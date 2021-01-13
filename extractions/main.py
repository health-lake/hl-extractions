# -*- coding: utf-8 -*-

from datetime import date

from extractCNAC import ExtractCNAC
from extractRCIV import ExtractRCIV
from extractSRAG import ExtractSRAG

def main():
    # Extractions of Transparência Registro Civil
    ExtractRCIV(initial_date=date(2015,1,1), final_dalte=date(2021,1,31)).download()
    
    # Extractions of dados.gov.br / SRAG
    ExtractSRAG.download()

    # Extractions of dados.gov.br / Casos Nacionais
    ExtractCNAC.download()

main()