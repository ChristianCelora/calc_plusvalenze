"""
    Converte report coinbase
    args:
        1 - filename .csv con le operazioni di importare
"""
import sys
import csv
from PlusvCalc.CoinbCsvReader import CoinbCsvReader

def main():
    if len(sys.argv) < 2:
        print("Specificare un file csv in input")
        sys.exit(1)

    # Read operations
    coinb_reader = CoinbCsvReader()
    transactions = coinb_reader.getTransactionsFromCsv(sys.argv[1])
    for t in transactions :
        print(t)

    sys.exit(0)

if __name__ == "__main__":
    main()