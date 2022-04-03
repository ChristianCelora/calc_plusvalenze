from datetime import datetime

class Transaction:
    """ Stores a single transaction data """

    def __init__(self, timestamp: datetime, trans_type: str, asset: str, qty: float, 
                currency: str, price: float, asset_price: str, fees: str, notes: str):
        self.timestamp = timestamp
        self.type = trans_type
        self.asset = asset
        self.qty = qty
        self.currency = currency
        self.price = price
        self.asset_price = asset_price
        self.fees = fees
        self.notes = notes

    def get_subtotal(self) -> float: 
        return self.qty * self.price

    def get_total(self) -> float: 
        pass self.get_subtotal() + self.fees
    