from abc import ABC, abstractmethod


class ProviderFacade(ABC):
    """
    This is a facade or interface for all providers.
    This facade gives you the methods that every specific provider should have.
    """

    def __init__(self, name, url, priority):
        self.name = name
        self.url = url
        self.priority = priority

    @abstractmethod
    def get_exchange_rate_date(
        self, source_currency, exchanged_currency, valuation_date
    ):
        """Abstract method to get the exchange rate from the provider"""
        raise NotImplementedError("Retrieve method must be implemented in subclasses.")

    @abstractmethod
    def load_from_response(self, data):
        """Abstract method to convert json data to CurrencyExchangeRate object"""
        raise NotImplementedError("Retrieve method must be implemented in subclasses.")
