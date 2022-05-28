from ctypes import sizeof
import pytest
import os

from PlusvCalc.CoinbCsvReader import CoinbCsvReader
from PlusvCalc.Transaction import Transaction

def checkTransaction(t: Transaction):
    assert t.timestamp != "", t.timestamp
    assert t.type != "", t.type
    assert t.asset != "", t.asset
    assert t.qty > 0, t.qty
    assert t.currency != "", t.currency
    assert t.asset_price != "", t.asset_price
    assert t.fees >= 0, t.fees
    assert t.notes != "", t.notes
    # assert t.subtotal > 0, t.subtotal
    # assert t.total > 0, t.total

"""
    TEST data
    I csv di test vanno posizionati nella cartella test_data
        - test_data_clean.csv: dati puliti. Transazioni semplici
        - test_data_error.csv: dati sporchi. 0 Transazioni valide
        - test_data_mixed.csv: dati misti. Prime righe non valide.
"""

def test_readCsvClean():
    csv_path = os.path.join("test_data", "test_data_clean.csv")
    csv_reader = CoinbCsvReader()
    transactions = csv_reader.getTransactionsFromCsv(csv_path)

    assert type(transactions) == list
    assert len(transactions) == 4
    for t in transactions:
        assert type(t) == Transaction
        checkTransaction(t)

def test_readCsvError():
    csv_path = os.path.join("test_data", "test_data_error.csv")
    csv_reader = CoinbCsvReader()
    transactions = csv_reader.getTransactionsFromCsv(csv_path)

    assert type(transactions) == list
    assert len(transactions) == 0

def test_readCsvMixed():
    csv_path = os.path.join("test_data", "test_data_mixed.csv")
    csv_reader = CoinbCsvReader()
    transactions = csv_reader.getTransactionsFromCsv(csv_path)

    assert type(transactions) == list
    assert len(transactions) == 23
    for t in transactions:
        assert type(t) == Transaction
        checkTransaction(t)
        
    