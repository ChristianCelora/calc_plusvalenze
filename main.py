"""
    Converte report coinbase
    args:
        1 - filename .csv con le operazioni di importare
"""
import sys
import csv

def main():
    if len(sys.argv) < 2:
        print("Specificare un file csv in input")
        sys.exit(1)

    # Read operations
    with open(sys.argv[1], "r") as csv_file:
        reader = csv.reader(csv_file)


    sys.exit(0)

if __name__ == "__main__":
    main()