from abc import ABC, abstractmethod


class Provider(ABC):

    def __init__(self, name, url, priority):
        self.name = name
        self.url = url
        self.priority = priority

    @abstractmethod
    def get_exchange_rate_date(self, source_currency, exchange_currency, valuation_date):
        """Abstract method to get the exchange rate from the provider"""
        raise NotImplementedError("Retrieve method must be implemented in subclasses.")

    @abstractmethod
    def load_from_json(self, json_data):
        """Abstract method to convert json data to CurrencyExchangeRate object"""
        raise NotImplementedError("Retrieve method must be implemented in subclasses.")

