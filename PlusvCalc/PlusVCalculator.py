from PlusvCalc.Transaction import Transaction

class PlusVCalculator:
    def __init__(self) -> None:
        pass

    def calcPlusV(self, transactions: Transaction):
        """
            Calcolo plusvalenze 

            recupera transazioni e calcola le plusvalenze con la formula
                plus = (sell_price - bought_price) - fees

            in caso di più transazioni si utilizza il criterio LIFO, 
            partendo dalla più recente operazione di acquisto
        """
        t_dict = self.processTransactions(transactions)

        # calc plus valenze
        plus_by_asset = self.calculatePlusValenzeFromDict(t_dict)

        return sum(plus_by_asset.values())

    def processTransactions(self, t_list: list) -> dict:
        """
            Formattazione lista transazioni in un dizionario.
            La sua struttura:
                symbol -> bought / sold -> date -> Transaction
            
            Le transazioni di tipo "Convert" devono essere trasformate in 2 transazioni.
            Una di vendita della moneta in questione e una di acquisto della nuova moneta
        """
        tr_dict = {}
        for t in t_list:
            if t.type == Transaction.TYPE_CONVERT:
                t_conv = t.getConvertedTransaction()
                if t_conv is not None:
                    t.type = Transaction.TYPE_SELL
                    tr_dict = self.__addTransactionToDict(tr_dict, t)
                    tr_dict = self.__addTransactionToDict(tr_dict, t_conv)
            elif t.type == Transaction.TYPE_BUY or t.type == Transaction.TYPE_SELL:
                tr_dict = self.__addTransactionToDict(tr_dict, t)
            
        return tr_dict

    def __addTransactionToDict(self, dict: dict, t: Transaction) -> dict:
        """
            Aggiunge una transazione alla struttura del dizionario
        """
        if t.asset not in dict:
                dict[t.asset] = {}

        if t.type not in dict[t.asset]:
            dict[t.asset][t.type] = {}
        
        t_time = t.timestamp.strftime("%Y%m%dT%H%m%s")
        # dict[t.asset] is ordered by date
        dict[t.asset][t.type][t_time] = t 

        return dict

    def calculatePlusValenzeFromDict(self, dict: dict) -> dict:
        """
            Calcola le plusvalenze per ogni asset del dizionario
        """
        plus_valenze = {}
        for asset in dict:
            plus_valenze[asset] = self.__calculatePlusValenzeForAsset(dict[asset])
        return plus_valenze

    def __calculatePlusValenzeForAsset(self, dict: dict) -> float:
        """
            Calcola la plusvalenza per un asset

            Nel caso ci sono più momenti di acquisto si utilizza il criterio di LIFO (Last In, First Out), 
            ossia, consideriamo cedute per prime le criptovalute acquisite più recentemente.

            plusvalenza = ((sell_price - bought_price) * sell_qty) - fees
        """
        plusvalenza = 0
        # for d_sell in dict[Transaction.TYPE_SELL]:
        if Transaction.TYPE_SELL in dict and len(dict[Transaction.TYPE_SELL].keys()) > 0:  
            for d_sell in sorted(dict[Transaction.TYPE_SELL].keys(), reverse=True):
                t_sell = dict[Transaction.TYPE_SELL][d_sell]
                sold_qty = t_sell.qty
                while sold_qty > 0:
                    d_buy, t_buy = self.__getClosestBuyTransaction(dict[Transaction.TYPE_BUY], d_sell)
                    if t_buy is None:
                        raise Exception("No buy transaction found for asset: " + t_sell.asset)

                    # calcolo plusvalenza
                    plusvalenza += round((t_sell.asset_price - t_buy.asset_price) * min(sold_qty, t_buy.qty), 2)
                    qty_bought = t_buy.qty
                    if sold_qty - qty_bought  > 0:
                        del dict[Transaction.TYPE_BUY][d_buy]   # rimuovo la transazione acquisto dalla lista
                        # Andrebbero rimosse le fees d'acquisto?
                    else:
                        # Aggiorna la Transaction
                        # Same as: dict[Transaction.TYPE_BUY][d_buy].qty -= min(qty_bought, sold_qty)
                        t_buy.qty -= min(qty_bought, sold_qty)

                    sold_qty -= qty_bought                
                    
                # Rimuovo le fees
                plusvalenza -= t_sell.fees

        return round(plusvalenza, 2)

    def __getClosestBuyTransaction(self, dict: dict, datestr: str) -> tuple:
        """
            Restituisce la transazione piu recente rispetto alla data datestr di acquisto

            datestr format: %Y%m%dT%H%m%s
        """
        closest_t_date = None
        closest_t = None
        for dt in sorted(dict.keys(), reverse=True):
            if dt > datestr:
                continue
            
            closest_t_date = dt
            closest_t = dict[dt]
            break

        return (closest_t_date, closest_t)