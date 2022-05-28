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
        # get transactions 
        # format transaction in structure
        #   symbol -> bought / sold -> date -> Transaction
        tr_dict = {}
        for t in transactions:
            # Filter unwanted typed
            if t.type != Transaction.TYPE_CONVERT and t.type != Transaction.TYPE_BUY and t.type != Transaction.TYPE_SELL: 
                continue
            
            if t.asset not in tr_dict:
                tr_dict[t.asset] = {}

            if t.type not in tr_dict[t.asset]:
                tr_dict[t.asset][t.type] = {}
            
            t_time = t.timestamp.strftime("%Y%m%dT%H%m%s")
            tr_dict[t.asset][t.type][t_time] = t # tr_dict[t.asset] is ordered by date
        print(tr_dict)

        # calc plus valenze

        pass