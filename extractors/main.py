from extr_cnac import ExtractCNAC
from extr_rciv import ExtractRCIV
from extr_srag import ExtractSRAG

from datetime import datetime

import sys, getopt


def main(source):
    if source == "CNAC":
        cnac = ExtractCNAC()
        cnac.download()
    elif source == "RCIV":
        rciv = ExtractRCIV(
            initial_date=datetime(2021, 1, 1), final_dalte=datetime(2021, 2, 28)
        )
        rciv.download()
    elif source == "SRAG":
        srag = ExtractSRAG()
        srag.download()


if __name__ == "__main__":
    main(sys.argv[1].upper())
