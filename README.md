# Calcolo plusvalenze

Sistema per calcolare le plusvalenze da csv.

Per ora calcola dal csv generato da coinbase

## Analisi formato file

### Coinbase

Formato file csv (x colonne):
 - Timestamp: data e ora della transazione (formato 
 - Transaction Type: Tipo di transazione. possibili valori: **Buy**, **Send**, **Convert**
 - Asset: Nome asset
 - Quantity Transacted: quantitæ transazione
 - Spot Price Currency: Valuta usata x il prezzo
 - Spot Price at Transaction: Prezzo dell'asset al momento della transazione
 - Subtotal: Totale transazione (Total - Fees)
 - Total (inclusive of fees): Totale transazione, incluso di commissioni (Quantity Transacted * Spot Price at Transaction)
 - Fees: commissioni
 - Notes


Esempio: 
```

|Timestamp             | Transaction Type | Asset | Quantity Transacted | 
------------------------------------------------------------------------
|2020-12-04T08:29:45Z  |  Convert	      |  BTC  |  0.003863	        |       	    
|2020-12-17T07:47:24Z  |  Convert	      |  BTC  |  0.004028	        |


|Spot Price Currency | Spot Price at Transaction | Subtotal | 
--------------------------------------------------------------
|USD                 | 19414.96	                 | 74.22    |
|USD                 | 22343.59	                 | 89.14    |


|Total (inclusive of fees) | Fees | Notes                                    |
------------------------------------------------------------------------------
|  90                      | 0.86 | Converted 0,004028 BTC to 89,144745 USDC |
|  75                      | 0.78 | Converted 0,003863 BTC to 0,12126672 ETH |
```

## Calcolo plus / minus valenza

Per il calcolo della plusvalenza (o minusvalenza) si calcola il prezzo di vendita, o scambio della moneta (si tratta comunque di una cessione ad onere), con il prezzo di acquisto.

Nel caso ci sono più momenti di acquisto si utilizza il criterio di **LIFO** (Last In, First Out), ossia, consideriamo cedute per prime le criptovalute acquisite più recentemente.

Inoltre, bisogna considerare che Coinbase utilizza dei prezzi in dollari (USD). In questo caso bisogna convertire il prezzo in dollari con quello in euro al giorno nel quale è stata effettutata l'operazione di acquisto / vendita.

## DEV

Per lanciare gli unit test usare il comando 

```
python -m pytest tests/
```