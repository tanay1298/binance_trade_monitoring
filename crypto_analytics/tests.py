# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test import RequestFactory
from crypto_analytics.views import get_latest_price, get_historical_price_data, perform_statistical_analysis
from crypto_analytics.models import Trade
import pytest
import json
from unittest.mock import patch
from datetime import datetime

@pytest.mark.django_db
def test_get_latest_price():
    factory = RequestFactory()
    request = factory.get('/api/latest-price/BTC/')

    Trade.objects.create(
                            trade_id=735823038, 
                            symbol='BTCUSDT', 
                            event_time=1711811982308, 
                            event_type='trade', 
                            price=100, 
                            quantity=0.5, 
                            buy_order_id=12, 
                            sell_order_id=15, 
                            trade_completed_time=1711811111108, 
                            is_maker=1, 
                            is_taker=0
                        )

    response = get_latest_price(request, symbol='BTCUSDT')

    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data == {'success': True, 'data': {'symbol': 'BTCUSDT', 'price': '100.00000000', 'timestamp': 1711811982308}}

@pytest.mark.django_db
def test_get_latest_price_no_trade_records(monkeypatch):
    factory = RequestFactory()
    request = factory.get('/api/latest-price/BTC/')
    latest_trade = None

    def mock_filter(*args, **kwargs):
        return Trade.objects.none()
    
    monkeypatch.setattr(Trade.objects, 'filter', mock_filter)
    response = get_latest_price(request, symbol='BTC')

    assert response.status_code == 404
    response_data = json.loads(response.content)
    assert response_data == {'success': False, 'message': 'No trade records found for symbol BTC.'}


@pytest.mark.django_db
def test_get_historical_price_data():
    Trade.objects.create(
        trade_id=1,
        symbol='BTCUSDT',
        event_time=datetime.now().timestamp(),
        event_type='trade',
        price=100,
        quantity=0.5,
        buy_order_id=12,
        sell_order_id=15,
        trade_completed_time=datetime.now().timestamp(),
        is_maker=1,
        is_taker=0
    )

    factory = RequestFactory()
    request = factory.get('/api/historical-price/', {'start_date': '2024-01-01 00:00:00', 'end_date': '2024-12-31 23:59:59'})
    response = get_historical_price_data(request)

    assert response.status_code == 200

    response_data = json.loads(response.content)
    assert isinstance(response_data['data'], list)

@pytest.mark.django_db
def test_get_historical_price_data_invalid_date_format():
    factory = RequestFactory()
    request = factory.get('/api/historical-price/', {'start_date': '2024-01-01', 'end_date': 'invalid_date'})
    response = get_historical_price_data(request)

    assert response.status_code == 400
    response_data = json.loads(response.content)
    assert response_data['error'] == 'Invalid date format. Please use YYYY-MM-DD HH:MM:SS.'

@pytest.mark.django_db
def test_perform_statistical_analysis():
    Trade.objects.create(
        trade_id=735823038,
        symbol='BTC',
        event_time=datetime.now().timestamp(),
        event_type='trade',
        price=100,
        quantity=0.5,
        buy_order_id=12,
        sell_order_id=15,
        trade_completed_time=1711811111108,
        is_maker=1,
        is_taker=0
    )
    Trade.objects.create(
        trade_id=735823039,
        symbol='BTC',
        event_time=datetime.now().timestamp(),
        event_type='trade',
        price=200,
        quantity=0.5,
        buy_order_id=12,
        sell_order_id=15,
        trade_completed_time=1711811111108,
        is_maker=1,
        is_taker=0
    )
    Trade.objects.create(
        trade_id=735823040,
        symbol='BTC',
        event_time=datetime.now().timestamp(),
        event_type='trade',
        price=300,
        quantity=0.5,
        buy_order_id=12,
        sell_order_id=15,
        trade_completed_time=1711811111108,
        is_maker=1,
        is_taker=0
    )

    factory = RequestFactory()
    request = factory.get('/api/statistical-data/', {'symbol': 'BTC'})
    response = perform_statistical_analysis(request)
    assert response.status_code == 200

    expected_data = {
        'symbol': 'BTC',
        'average_price': 200.0,
        'median_price': 200,
        'standard_deviation': 81.6496580927726
    }
    response_data = json.loads(response.content)

    assert response_data['symbol'] == expected_data['symbol']
    assert float(response_data['average_price']) == expected_data['average_price']
    assert float(response_data['median_price']) == expected_data['median_price']
    assert float(response_data['standard_deviation']) == expected_data['standard_deviation']


@pytest.mark.django_db
def test_perform_statistical_analysis_negative():
    Trade.objects.create(
        trade_id=735823038,
        symbol='BTC',
        event_time=datetime.now().timestamp(),
        event_type='trade',
        price=100,
        quantity=0.5,
        buy_order_id=12,
        sell_order_id=15,
        trade_completed_time=1711811111108,
        is_maker=1,
        is_taker=0
    )

    factory = RequestFactory()
    request = factory.get('/api/statistical-data/', {'symbol': 'ETH'})
    response = perform_statistical_analysis(request)

    assert response.status_code == 404

    expected_data = {'error': 'No historical data found for symbol ETH.'}
    response_data = json.loads(response.content)
    assert response_data == expected_data
