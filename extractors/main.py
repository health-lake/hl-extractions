from extr_cnac import ExtractCNAC
from extr_rciv import ExtractRCIV
from extr_srag import ExtractSRAG

def main():
    cnac = ExtractCNAC()
    cnac.download()

    # todo: where is this date() defined? is crashing the script whenever run using docker.
    rciv = ExtractRCIV(
        initial_date = date(2015,1,1),
        final_dalte = date(2021,2,28)
    )
    rciv.download()

    srag = ExtractSRAG()
    srag.download()

main()