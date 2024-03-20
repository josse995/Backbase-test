from datetime import datetime, timezone, timedelta, date

from django.db.models import Q

from .enums import AVAILABLE_PROVIDERS
from ..currency.models import Currency, CurrencyExchangeRate


def get_all_currency_exchange_rates_for_source_currency(
    source_currency, date_from, date_to
):
    queryset = CurrencyExchangeRate.objects.filter(
        Q(source_currency__code=source_currency)
        & Q(valuation_date__range=(date_from, date_to))
    )
    days_between = date_to - date_from
    if queryset.count() <= days_between.days:
        available_dates = list(queryset.values_list("valuation_date", flat=True))
        _request_currency_exchange_rates(
            source_currency, date_from, date_to, available_dates
        )
        queryset = CurrencyExchangeRate.objects.filter(
            Q(source_currency__code=source_currency)
            & Q(valuation_date__range=(date_from, date_to))
        )
    return queryset


def get_currency_exchange_rates(
    source_currency, exchanged_currency, date_from, date_to
):
    queryset = CurrencyExchangeRate.objects.filter(
        Q(source_currency__code=source_currency)
        & Q(exchanged_currency__code=exchanged_currency)
        & Q(valuation_date__range=(date_from, date_to))
    )
    days_between = date_to - date_from
    if queryset.count() <= days_between.days:
        available_dates = list(queryset.values_list("valuation_date", flat=True))
        all_dates = list(date_ranges_in_days(date_from, date_to))
        missing_dates = [
            missing_date
            for missing_date in all_dates
            if missing_date not in available_dates
        ]
        for missing_date in missing_dates:
            _request_currency_exchange_rate(
                source_currency, exchanged_currency, missing_date
            )
        queryset = CurrencyExchangeRate.objects.filter(
            Q(source_currency__code=source_currency)
            & Q(exchanged_currency__code=exchanged_currency)
            & Q(valuation_date__range=(date_from, date_to))
        )
    return queryset


def get_latest_currency_exchange_rate(source_currency, exchanged_currency):
    today_date = datetime.now(timezone.utc).date()

    queryset = CurrencyExchangeRate.objects.filter(
        Q(source_currency__code=source_currency)
        & Q(exchanged_currency__code=exchanged_currency)
        & Q(valuation_date=today_date)
    )
    if queryset.count() <= 0:
        _request_currency_exchange_rate(source_currency, exchanged_currency, today_date)
        queryset = CurrencyExchangeRate.objects.filter(
            Q(source_currency__code=source_currency)
            & Q(exchanged_currency__code=exchanged_currency)
            & Q(valuation_date=today_date)
        )
    return queryset


def _request_currency_exchange_rates(
    source_currency, date_from, date_to, available_dates
):
    # todo: el nombre del metodo no explica lo que hace. Cambiarlo
    currencies = Currency.objects.all()
    all_dates = list(date_ranges_in_days(date_from, date_to))
    missing_dates = [
        missing_date
        for missing_date in all_dates
        if missing_date not in available_dates
    ]
    for missing_date in missing_dates:
        for currency in currencies:
            _request_currency_exchange_rate(
                source_currency, currency.code, missing_date
            )


def _request_currency_exchange_rate(source_currency, exchanged_currency, date):
    # todo: el nombre del metodo no explica lo que hace. Cambiarlo
    sorted_providers = sorted(
        AVAILABLE_PROVIDERS.items(), key=lambda item: item[1].priority
    )
    for name, provider in sorted_providers:
        try:
            response = provider.get_exchange_rate_date(
                source_currency, exchanged_currency, date
            )
            if not provider.load_from_response(response):
                # NOTE: An improvement here could be to store the response somewhere and in a background task
                # try to ingest again or be available if manual/automatic process can solve the issue
                print(f"An error occurred while saving this object: {response}")

        except (
            Exception
        ) as e:  # todo: change for the proper exception when requesting the data
            print(e)
            print(
                f"Provider {provider.name} failed to retrieve the exchange rate. Switching to next provider..."
            )
            continue


def date_ranges_in_days(date_from, date_to):
    for n in range(int((date_to - date_from).days) + 1):
        yield date_from + timedelta(days=n)
