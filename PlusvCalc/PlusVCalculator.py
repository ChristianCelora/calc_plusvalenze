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

        pass

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
            # Filter unwanted typed
            if t.type == Transaction.TYPE_CONVERT:
                pass
            elif t.type == Transaction.TYPE_BUY or t.type == Transaction.TYPE_SELL:
                tr_dict = self.__addTransactionToDict(tr_dict, t)
            
        return tr_dict

    def __addTransactionToDict(self, dict: dict, t: Transaction) -> dict:
        if t.asset not in dict:
                dict[t.asset] = {}

        if t.type not in dict[t.asset]:
            dict[t.asset][t.type] = {}
        
        t_time = t.timestamp.strftime("%Y%m%dT%H%m%s")
        # dict[t.asset] is ordered by date
        dict[t.asset][t.type][t_time] = t 

        return dict