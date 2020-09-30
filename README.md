# Cryptocurrency converting microservice. Binance API

The microservice allows you to convert specified amount of coins into another coin. It uses live price rates from of Binance API.Works only with signing


# How to run: 

1. Specify in request headers key "Sign" 
to "527e639f2f1aac80dee9d2ece85fdb755f802572f5b8e62c1a511ef8755be4e8b8e9ac43107a0734d456db7a62a1f7cc8d2da42a6ed035caf3642912f7cbdefa"
2. Send POST request with data to /calc route
POST body should contain (in_currency, out_currency, in_amount) parameters.
- in_currency - input coin you have
- out_currency - output coin you intend to convert in (result)
- in_amount - amount of coins. It's not neceserry parameter. Amount equals to 1 by default
 

### See more details about the cryptocurrency tickers below
https://api.binance.com/api/v1/ticker/price

E.g. It will convert 10 Moneros(XMR) into Tether by currently Binance price rates.
POST body: 
```python
{
    'in_currency' : 'XMR',
    'out_currency' : 'USDT',
    'in_amount' : 10,
}
```
It should return next results. Converting accepts integer/decimal
```python
{
    "out_amount": 990,
    "rate": 99
}
```