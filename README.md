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
 - Subtotal: Totale transazione
 - Total (inclusive of fees): Totale transazione, incluso di commissioni
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