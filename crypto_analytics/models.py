# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Trade(models.Model):
    event_type = models.CharField(max_length=100)
    event_time = models.BigIntegerField()
    symbol = models.CharField(max_length=100)
    trade_id = models.BigIntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=8)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    buy_order_id = models.BigIntegerField()
    sell_order_id = models.BigIntegerField()
    trade_completed_time = models.BigIntegerField()
    is_maker = models.BooleanField()
    is_taker = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'trade'