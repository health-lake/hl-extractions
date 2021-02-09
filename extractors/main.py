from extractCNAC import ExtractCNAC
from extractRCIV import ExtractRCIV
from extractSRAG import ExtractSRAG

def main():
    cnac = ExtractCNAC()
    cnac.download()

    rciv = ExtractRCIV(
        initial_date = date(2015,1,1),
        final_dalte = date(2021,2,28)
    )
    rciv.download()

    srag = ExtractSRAG()
    srag.download()

main()