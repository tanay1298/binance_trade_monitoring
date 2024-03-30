# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from crypto_analytics.models import Trade
from django.http import JsonResponse

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
