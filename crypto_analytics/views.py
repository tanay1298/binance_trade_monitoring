# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from crypto_analytics.models import Trade
from django.http import JsonResponse
from datetime import datetime

def get_latest_price(request, symbol):
    # Get latest trade record for the specified symbol
    latest_trade = Trade.objects.filter(symbol=symbol).order_by('-event_time').first()

    if latest_trade:
        data = {
            'symbol': latest_trade.symbol,
            'price': latest_trade.price,
            'timestamp': latest_trade.event_time
        }
        return JsonResponse({'success': True, 'data': data})
    else:
        return JsonResponse({'success': False, 'message': f'No trade records found for symbol {symbol}.'}, status=404)

def get_historical_price_data(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Please use YYYY-MM-DD HH:MM:SS.'}, status=400)

    # Convert datetime objects to Unix timestamps
    start_timestamp = int(start_date.timestamp() * 1000.0)
    end_timestamp = int(end_date.timestamp() * 1000.0)

    historical_data = Trade.objects.filter(trade_completed_time__range=(start_timestamp, end_timestamp)).values('trade_completed_time', 'price')
    serialized_data = [{'timestamp': entry['trade_completed_time'], 'price': entry['price']} for entry in historical_data]
    return JsonResponse({'data': serialized_data})