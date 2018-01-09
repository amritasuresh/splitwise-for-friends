# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

import time, requests, json, decimal, sys
from importlib import reload

@login_required(login_url='/login')
def get_exchange_rates(request):
    """
    This function fetches the latest daily exchange rates in order to convert between currencies.
    The exchange rates are retrieved from the European Central Bank, using the Fixer API: http://fixer.io/
    :param request: the HTTP request
    :return: a list of exchange rates for many currencies when exchanging euros
    """

    # We store the previous exchange rates and only get new ones if some time has elapsed since we last retrieved them.
    if 'rates' in request.session and 'last_time' in request.session:
        now = int(time.time())
        # If more than an hour has elapsed
        if abs(now - request.session['last_time']) > 3600:
            r = requests.get('https://api.fixer.io/latest')
            text = json.loads(r.text)
            rates = text['rates']
            request.session['rates'] = rates
            request.session['last_time'] = now
            return rates
        else:
            return request.session['rates']
    else:
        now = int(time.time())
        r = requests.get('https://api.fixer.io/latest')
        text = json.loads(r.text)
        rates = text['rates']
        request.session['rates'] = rates
        request.session['last_time'] = now
        return rates


@login_required(login_url='/login')
def get_symbol(request, my_account):
    """
    This function returns the appropriate symbol for the current currency
    :param my_account: the user's Account
    :return: A string representing the user's currency symbol
    """
    symbols = {'EUR': u'€', 'USD': u'$', 'PLN': u'zł', 'INR': u'₹'}
    return symbols.get(my_account.currency, 'default').decode('utf8')


@login_required(login_url='/login')
def convert_amount(request, amount, currency_in, currency_out):
    """
    This function converts the given amount (in any currency) into the correct amount in the user's currency
    :param request: the HTTP request
    :param amount: the input amount
    :param currency_in: the input currency
    :param currency_out: the output currency
    :return: the output amount in the correct currency
    """
    rates = get_exchange_rates(request)

    # convert to EUR
    if currency_in != 'EUR':
        rate_in = rates[currency_in]
        amount *= 1.0 / rate_in

    # convert to output currency
    if currency_out != 'EUR':
        rate_out = rates[currency_out]
        amount *= decimal.Decimal(rate_out)

    return amount


@login_required(login_url='/login')
def amount_as_string(request, amount, my_account):
    """
    This function displays the given amount as a string with the appropriate currency symbol (e.g. "€100.00")
    :param request: the HTTP request
    :param amount: the input amount
    :param my_account: the user's Account
    :return: a string representing the amount in the given currency.
    """
    reload(sys)
    sys.setdefaultencoding('utf8')

    symbol = get_symbol(request, my_account)
    if my_account.currency == 'PLN':
        if amount <= -0.01:
            string = ("-%.2f " % abs(amount)) + symbol
        else:
            string = ("%.2f " % amount) + symbol
    else:
        if amount <= -0.01:
            string = "-" + symbol + ("%.2f" % amount)
        else:
            string = symbol + ("%.2f" % amount)

    return string
