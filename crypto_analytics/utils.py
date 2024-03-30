import websocket
import json
import ssl
import time

def on_error(ws, error):
    print(error)

def on_message(ws, message):
    message_data = json.loads(message)
    print(message_data)

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

if __name__ == "__main__":
    connect_to_binance_websocket()
