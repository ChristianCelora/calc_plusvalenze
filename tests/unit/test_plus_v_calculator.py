import pytest

from PlusvCalc.PlusVCalculator import PlusVCalculator
from PlusvCalc.Transaction import Transaction

def test_processTransactions():
    transactions = []
    plusv_calc = PlusVCalculator()
    plusv_calc.calcPlusV(transactions)
