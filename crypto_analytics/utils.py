import websocket
import json
import ssl
import time
import queue
import os
from django.conf import settings

import django
django.setup()

from crypto_analytics.models import Trade

BUFFER_SIZE = 100

# buffer to hold stream data
stream_buffer = queue.Queue(maxsize=BUFFER_SIZE)

def on_error(ws, error):
    print(error)

def on_message(ws, message):
    message_data = json.loads(message)
    print(message_data)
    add_to_buffer(message_data)

def on_close(ws, close_status_code, close_msg):
    print("### WebSocket closed ###")

def on_open(ws):
    print("### WebSocket opened ###")
    ws.send('{"method": "SUBSCRIBE", "params": ["btcusdt@trade", "ethusdt@trade", "bnbusdt@trade"], "id": 1}')

def connect_to_binance_websocket():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

def add_to_buffer(data):
    try:
        stream_buffer.put(data, block=False)
    except queue.Full:
        print("Buffer full, flushing...")
        save_to_database(stream_buffer)

def save_to_database(buffer):
    while not buffer.empty():
        message_data = buffer.get()
        event_type = message_data.get('e')
        event_time = message_data.get('E')
        symbol = message_data.get('s')
        trade_id = message_data.get('t')
        price = message_data.get('p')
        quantity = message_data.get('q')
        buy_order_id = message_data.get('b')
        sell_order_id = message_data.get('a')
        trade_completed_time = message_data.get('T')
        is_maker = message_data.get('m')
        is_taker = message_data.get('M')

        trade = Trade(
            event_type=event_type,
            event_time=event_time,
            symbol=symbol,
            trade_id=trade_id,
            price=price,
            quantity=quantity,
            buy_order_id=buy_order_id,
            sell_order_id=sell_order_id,
            trade_completed_time=trade_completed_time,
            is_maker=is_maker,
            is_taker=is_taker
        )
        trade.save()
    print('saved buffer object to db')

if __name__ == "__main__":
    connect_to_binance_websocket()
