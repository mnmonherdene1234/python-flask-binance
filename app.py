from flask import Flask, request, make_response, abort, session, send_file
from markupsafe import escape
from werkzeug.utils import secure_filename
import requests
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
client = Client("aoYBzuKc0A7Lr8MQGMKVnSgAfYcv9UFofYEaw42826ujl1PEcJbK7Xjdb49woWGS",
                "WqNdJD4Hd9frY50M9Fodj1ZEjmkJlryyW5IvqujlF3ENqklVkjakmtEXjH06o5qr")

app = Flask(__name__)


@app.get("/")
def price():
    symbol = 'BTCUSDT'
    price = float(client.get_avg_price(symbol=symbol)["price"])
    orders = client.get_order_book(symbol=symbol, limit=1000)
    asks = orders["asks"]
    bids = orders["bids"]

    asks_total = 0
    asks_max_price = [0, 0]
    for ask in asks:
        asks_total += float(ask[1])

        if (float(ask[1]) > float(asks_max_price[1])):
            asks_max_price = [float(ask[0]), float(ask[1])]

    bids_total = 0
    bids_max_price = [0, 0]
    for bid in bids:
        bids_total += float(bid[1])

        if (float(bid[1]) > float(bids_max_price[1])):
            bids_max_price = [float(bid[0]), float(bid[1])]

    return {
        "symbol": symbol,
        "price": price,
        "bids_total": bids_total,
        "asks_total": asks_total,
        "bids_max_price": bids_max_price,
        "asks_max_price": asks_max_price,
    }
