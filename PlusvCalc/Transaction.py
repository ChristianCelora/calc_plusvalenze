from datetime import datetime

class Transaction:
    """ Stores a single transaction data """

    def __init__(self, timestamp: datetime, trans_type: str, asset: str, qty: float, 
                currency: str, asset_price: float, fees: float, notes: str):
        self.timestamp = timestamp
        self.type = trans_type
        self.asset = asset
        self.qty = float(qty)
        self.currency = currency
        self.asset_price = float(asset_price)
        self.fees = float(fees)
        self.notes = notes

    def get_total(self) -> float: 
        return round(self.qty * self.asset_price, 2)

    def get_subtotal(self) -> float: 
        return self.get_total() - self.fees

    def __str__(self) -> str:
        return "{} {} {} at {} {}".format(
            self.type, 
            self.qty, 
            self.asset, 
            self.asset_price, 
            self.currency
        )