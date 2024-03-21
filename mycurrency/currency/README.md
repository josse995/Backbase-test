# Currency

This module has the common models to be used on the app plus views for doing actions on django admin portal.

## Models

### [Currency](models.py)
This model has all information about each currency, such as the code, name and symbol of the currency.

In order to have a system that works, a [fixture file](fixtures/currency_fixture.json) with all currencies is loaded everytime the app is started

### [CurrencyExchangeRate](models.py)
This model contain the rate value between two currencies for a specific date plus the name of the provider where the 
exchange rate was retrieved, in case some analysis is wanted to be made.

Each currency is linked with the model Currency, so each object will contain always a currency defined on Currency model.

As same as in Currency model, this model has a [fixture file](fixtures/currencyexchangerate_fixture.json) to load mock currency exchange rate when the app is started

## Django admin views (backoffice/admin)

### Converter view:

Due to time limitations, this was not implemented.

### Graph view:

This view shows a graph with all value of a given CurrencyExchangeRate object selected on the list of CurrencyExchangeRate.

To view the graph:
1. On left menu, go to Currency > Currency exchange rates.
2. Select **ONLY ONE** element, and on the action drop menu, select 'Historical rates value graph action'.
3. Click on left button labeled 'Show Graph'.
