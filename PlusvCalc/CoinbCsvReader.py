import csv
from PlusvCalc.Transaction import Transaction
from datetime import datetime

class CoinbCsvReader:
    """ Parse coinbase csv report """
    def __init__(self):
        self.header_keys = ["Timestamp","Transaction Type","Asset","Quantity Transacted","Spot Price Currency","Fees","Notes"]
        pass

    def getTransactionsFromCsv(self, csv_path: str, delimiter: str = ",") -> list: 
        transactions = []
        with open(csv_path, "r+") as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)
            header_row_index = self.detectHeader(reader)
            # Skips header_row_index lines
            csv_file.seek(0)
            for i in range(header_row_index): next(csv_file)
            # Now csv starts at header. Read first lines
            reader = csv.DictReader(csv_file, delimiter=delimiter)
            for i, row in enumerate(reader):
                if self.isRowValid(row):
                    try:
                        fees = row["Fees"]
                        if fees == "":
                            fees = 0
                        
                        transactions.append(Transaction(
                            self.getDatetimeFromCoinbTimestamp(row["Timestamp"]),
                            row["Transaction Type"],
                            row["Asset"],
                            row["Quantity Transacted"],
                            row["Spot Price Currency"],
                            row["Spot Price at Transaction"],
                            fees,
                            row["Notes"]
                        ))
                    except Exception as e: 
                        print(e)
        return transactions

    def detectHeader(self, reader: csv.reader) -> int:
        """ Detects header row. First valid row is the header """
        i = 0
        for row in reader:
            if self.isRowValid(row):
                return i
            i += 1
        return i

    def isRowValid(self, row: list) -> bool:
        """ Checks if a row is valid """
        if all (k in row for k in (self.header_keys)):
            return True
        return False

    def getDatetimeFromCoinbTimestamp(self, timestamp: str) -> datetime:
        return datetime.fromisoformat(timestamp.replace("Z", ""))