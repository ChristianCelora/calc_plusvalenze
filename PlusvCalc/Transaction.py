from datetime import datetime

class Transaction:
    """ Stores a single transaction data """

    TYPE_CONVERT = "Convert"
    TYPE_BUY = "Buy"
    TYPE_SELL = "Sell"
    TYPE_SEND = "Send"
    TYPE_EARN = "Coinbase Earn"

    def __init__(self, timestamp: datetime, trans_type: str, asset: str, qty: float, 
                currency: str, asset_price: float, fees: float, notes: str):
        if not isinstance(timestamp, datetime):
            raise TypeError("timestamp must be a datetime instance")

        self.timestamp = timestamp
        self.type = trans_type
        self.asset = asset
        self.qty = float(qty)
        self.currency = currency
        self.asset_price = float(asset_price)
        self.fees = float(fees)
        self.notes = notes

    def getTotal(self) -> float: 
        return round(self.qty * self.asset_price, 2)

    def getSubtotal(self) -> float: 
        return self.getTotal() - self.fees

    def getConvertedTransaction(self) -> "Transaction|None":
        """
            Returns the converted transaction. 
            Sadly Coinb saves the info in the notes... ugh!
        """
        if self.type != Transaction.TYPE_CONVERT:
            return None 

        # this is bad!
        notes_split = self.notes.split(" ")
        if len(notes_split) != 6:
            return None

        converted_qty = float(notes_split[-2].replace(",", "."))
        # for some reason this is different than self.qty
        qty = float(notes_split[1].replace(",", "."))

        t_new = Transaction(
            self.timestamp, 
            Transaction.TYPE_BUY, 
            notes_split[-1], 
            converted_qty, 
            self.currency,
            self.__calcCnvertedPrice(qty, converted_qty),
            0,
            self.notes
        )

        return t_new

    def __calcCnvertedPrice(self, qty: float, qty_converted: float) -> float:
        return round(qty * self.asset_price / qty_converted, 3)

    def __str__(self) -> str:
        return "{} {} {} at {} {}".format(
            self.type, 
            self.qty, 
            self.asset, 
            self.asset_price, 
            self.currency
        )