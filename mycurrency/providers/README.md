# Providers

This module includes all providers used to retrieve exchange rate values for currencies. 

Each of the providers have been built following the Adapter pattern, and also each of them have
to implement a ProviderBase (Facade pattern), to be sure every new implemented providers is pluggable 
without modifying the rest of the code.

Each provider has a priority assigned ('0' meaning first to request the data from), and if an exchanged rate 
value is not found on our database, it is possible to ask to providers, retrieve it and store it.

There are two providers in this app:

- Mock provider: it gives you a random rate value from two given currencies and a date.
- Fixer provider: request to [Fixer.io](http://fixer.io) for a rate value from two given currencies and a date. 
For this assignment, the retrieve method was implemented and tested, but there is no API_KEY given because 
limitations on free plan.
