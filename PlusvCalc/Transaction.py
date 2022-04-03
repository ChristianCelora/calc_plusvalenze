from datetime import datetime

class Transaction:
    """ Stores a single transaction data """

    def __init__(self, timestamp: datetime, trans_type: str, asset: str, qty: float, 
                currency: str, asset_price: float, fees: float, notes: str):
        self.timestamp = timestamp
        self.type = trans_type
        self.asset = asset
        self.qty = qty
        self.currency = currency
        self.asset_price = asset_price
        self.fees = fees
        self.notes = notes

    def get_subtotal(self) -> float: 
        return round(self.qty * self.asset_price, 2)

    def get_total(self) -> float: 
        return self.get_subtotal() + self.fees
    