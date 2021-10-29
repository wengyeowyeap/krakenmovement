import os
import config
from flask import Flask, render_template
from turbo_flask import Turbo
import threading
import time

app = Flask('CRYPTO MOVEMENT')
turbo = Turbo(app)

onemin_change = []
fivemin_change = []
fifteenmin_change = []
thirtymin_change = []
onehour_change = []
fourhour_change = []

import requests
krakenlist = requests.get("https://api.kraken.com/0/public/AssetPairs").json().get("result")
filteredstring = ""

for pair_name, pair_info in krakenlist.items():
    if pair_name[-3:] == "USD" or pair_name[-3:] == "XBT" or pair_name[-3:] == "ETH" or pair_name[-4:] == "USDC" or pair_name[-4:] == "USDT":
        filteredstring = filteredstring + '"' + pair_info.get('wsname') + '"' + ','
        onemin_change.append({"name" : pair_info.get('wsname'), "change" : 0})
        fivemin_change.append({"name" : pair_info.get('wsname'), "change" : 0})
        fifteenmin_change.append({"name" : pair_info.get('wsname'), "change" : 0})
        thirtymin_change.append({"name" : pair_info.get('wsname'), "change" : 0})
        onehour_change.append({"name" : pair_info.get('wsname'), "change" : 0})
        fourhour_change.append({"name" : pair_info.get('wsname'), "change" : 0})
filteredstring = filteredstring[0:-1]

@app.context_processor
def inject_load():
    # Import WebSocket client library (and others)
    import websocket
    import _thread

    # 1m
    # Define WebSocket callback functions
    def ws_message_onemin(ws, message):
        global onemin_change
        import json
        from datetime import datetime, timedelta
        
        # print("WebSocket thread (1m): %s" % message)
        message = json.loads(message)

        if message[2] == "ohlc-1":
            current_pair = message[3]
            start_time = datetime.fromtimestamp(float(message[1][0]))
            open_price = float(message[1][2])
            high_price = float(message[1][3])
            low_price = float(message[1][4])
            close_price = float(message[1][5])

            if (close_price - open_price == 0) or (datetime.now() - start_time > timedelta(minutes=1)):
                for pair in onemin_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': 0})
            elif close_price - open_price > 0:
                for pair in onemin_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': ((high_price - low_price) / low_price) * 100})
            elif close_price - open_price < 0:
                for pair in onemin_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': ((high_price - low_price) / low_price) * -100})

    def ws_open_onemin(ws):
        query = '{"event":"subscribe", "subscription":{"name":"ohlc", "interval":1}, "pair":['+ filteredstring + ']}'
        ws.send(query)

    def ws_thread_onemin(*args):
        ws = websocket.WebSocketApp("wss://ws.kraken.com/", on_open = ws_open_onemin, on_message = ws_message_onemin)
        ws.run_forever()

    # Start a new thread for the WebSocket interface
    _thread.start_new_thread(ws_thread_onemin, ())

    # 5min
    # Define WebSocket callback functions
    def ws_message_fivemin(ws, message):
        global fivemin_change
        import json
        from datetime import datetime, timedelta
        print("WebSocket thread (5m): %s" % message)
        message = json.loads(message)

        if message[2] == "ohlc-5":
            current_pair = message[3]
            start_time = datetime.fromtimestamp(float(message[1][0]))
            open_price = float(message[1][2])
            high_price = float(message[1][3])
            low_price = float(message[1][4])
            close_price = float(message[1][5])

            if (close_price - open_price == 0) or (datetime.now() - start_time > timedelta(minutes=5)):
                for pair in fivemin_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': 0})
            elif close_price - open_price > 0:
                for pair in fivemin_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': ((high_price - low_price) / low_price) * 100})
            elif close_price - open_price < 0:
                for pair in fivemin_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': ((high_price - low_price) / low_price) * -100})
    def ws_open_fivemin(ws):
        query = '{"event":"subscribe", "subscription":{"name":"ohlc", "interval":5}, "pair":['+ filteredstring + ']}'
        ws.send(query)

    def ws_thread_fivemin(*args):
        ws = websocket.WebSocketApp("wss://ws.kraken.com/", on_open = ws_open_fivemin, on_message = ws_message_fivemin)
        ws.run_forever()

    # Start a new thread for the WebSocket interface
    _thread.start_new_thread(ws_thread_fivemin, ())

    # 15min
    # Define WebSocket callback functions
    def ws_message_fifteenmin(ws, message):
        global fifteenmin_change
        import json
        from datetime import datetime, timedelta
        # print("WebSocket thread (15m): %s" % message)
        message = json.loads(message)

        if message[2] == "ohlc-15":
            current_pair = message[3]
            start_time = datetime.fromtimestamp(float(message[1][0]))
            open_price = float(message[1][2])
            high_price = float(message[1][3])
            low_price = float(message[1][4])
            close_price = float(message[1][5])

            if (close_price - open_price == 0) or (datetime.now() - start_time > timedelta(minutes=15)):
                for pair in fifteenmin_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': 0})
            elif close_price - open_price > 0:
                for pair in fifteenmin_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': ((high_price - low_price) / low_price) * 100})
            elif close_price - open_price < 0:
                for pair in fifteenmin_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': ((high_price - low_price) / low_price) * -100})

    def ws_open_fifteenmin(ws):
        query = '{"event":"subscribe", "subscription":{"name":"ohlc", "interval":15}, "pair":['+ filteredstring + ']}'
        ws.send(query)

    def ws_thread_fifteenmin(*args):
        ws = websocket.WebSocketApp("wss://ws.kraken.com/", on_open = ws_open_fifteenmin, on_message = ws_message_fifteenmin)
        ws.run_forever()

    # Start a new thread for the WebSocket interface
    _thread.start_new_thread(ws_thread_fifteenmin, ())

    # 30min
    # Define WebSocket callback functions
    def ws_message_thirtymin(ws, message):
        global thirtymin_change
        import json
        from datetime import datetime, timedelta
        # print("WebSocket thread (30m): %s" % message)
        message = json.loads(message)

        if message[2] == "ohlc-30":
            current_pair = message[3]
            start_time = datetime.fromtimestamp(float(message[1][0]))
            open_price = float(message[1][2])
            high_price = float(message[1][3])
            low_price = float(message[1][4])
            close_price = float(message[1][5])

            if (close_price - open_price == 0) or (datetime.now() - start_time > timedelta(minutes=30)):
                for pair in thirtymin_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': 0})
            elif close_price - open_price > 0:
                for pair in thirtymin_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': ((high_price - low_price) / low_price) * 100})
            elif close_price - open_price < 0:
                for pair in thirtymin_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': ((high_price - low_price) / low_price) * -100})

    def ws_open_thirtymin(ws):
        query = '{"event":"subscribe", "subscription":{"name":"ohlc", "interval":30}, "pair":['+ filteredstring + ']}'
        ws.send(query)

    def ws_thread_thirtymin(*args):
        ws = websocket.WebSocketApp("wss://ws.kraken.com/", on_open = ws_open_thirtymin, on_message = ws_message_thirtymin)
        ws.run_forever()

    # Start a new thread for the WebSocket interface
    _thread.start_new_thread(ws_thread_thirtymin, ())

    # 1H
    # Define WebSocket callback functions
    def ws_message_onehour(ws, message):
        global onehour_change
        import json
        from datetime import datetime, timedelta
        # print("WebSocket thread (1H): %s" % message)
        message = json.loads(message)

        if message[2] == "ohlc-60":
            current_pair = message[3]
            start_time = datetime.fromtimestamp(float(message[1][0]))
            open_price = float(message[1][2])
            high_price = float(message[1][3])
            low_price = float(message[1][4])
            close_price = float(message[1][5])

            if (close_price - open_price == 0) or (datetime.now() - start_time > timedelta(hours=1)):
                for pair in onehour_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': 0})
            elif close_price - open_price > 0:
                for pair in onehour_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': ((high_price - low_price) / low_price) * 100})
            elif close_price - open_price < 0:
                for pair in onehour_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': ((high_price - low_price) / low_price) * -100})

    def ws_open_onehour(ws):
        query = '{"event":"subscribe", "subscription":{"name":"ohlc", "interval":60}, "pair":['+ filteredstring + ']}'
        ws.send(query)

    def ws_thread_onehour(*args):
        ws = websocket.WebSocketApp("wss://ws.kraken.com/", on_open = ws_open_onehour, on_message = ws_message_onehour)
        ws.run_forever()

    # Start a new thread for the WebSocket interface
    _thread.start_new_thread(ws_thread_onehour, ())

    # 4H
    # Define WebSocket callback functions
    def ws_message_fourhour(ws, message):
        global fourhour_change
        import json
        from datetime import datetime, timedelta
        # print("WebSocket thread (4H): %s" % message)
        message = json.loads(message)

        if message[2] == "ohlc-240":
            current_pair = message[3]
            start_time = datetime.fromtimestamp(float(message[1][0]))
            open_price = float(message[1][2])
            high_price = float(message[1][3])
            low_price = float(message[1][4])
            close_price = float(message[1][5])

            if (close_price - open_price == 0) or (datetime.now() - start_time > timedelta(hours=4)):
                for pair in fourhour_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': 0})
            elif close_price - open_price > 0:
                for pair in fourhour_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': ((high_price - low_price) / low_price) * 100})
            elif close_price - open_price < 0:
                for pair in fourhour_change:
                    if pair["name"] == current_pair:
                        pair.update({'name': current_pair, 'change': ((high_price - low_price) / low_price) * -100})

    def ws_open_fourhour(ws):
        query = '{"event":"subscribe", "subscription":{"name":"ohlc", "interval":240}, "pair":['+ filteredstring + ']}'
        ws.send(query)

    def ws_thread_fourhour(*args):
        ws = websocket.WebSocketApp("wss://ws.kraken.com/", on_open = ws_open_fourhour, on_message = ws_message_fourhour)
        ws.run_forever()

    # Start a new thread for the WebSocket interface
    _thread.start_new_thread(ws_thread_fourhour, ())

    return {'sorted1min': sorted(onemin_change, key=lambda x: x["change"]), 
            'sorted5min': sorted(fivemin_change, key=lambda x: x["change"]),
            'sorted15min': sorted(fifteenmin_change, key=lambda x: x["change"]),
            'sorted30min': sorted(thirtymin_change, key=lambda x: x["change"]),
            'sorted1hour': sorted(onehour_change, key=lambda x: x["change"]),
            'sorted4hour': sorted(fourhour_change, key=lambda x: x["change"]),
            }

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/1min")
def page1min():
    return render_template('page1min.html')

@app.route("/5min")
def page5min():
    return render_template('page5min.html')

@app.route("/15min")
def page15min():
    return render_template('page15min.html')

@app.route("/30min")
def page30min():
    return render_template('page30min.html')

@app.route("/1hour")
def page1hour():
    return render_template('page1hour.html')

@app.route("/4hour")
def page4hour():
    return render_template('page4hour.html')

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

def update_load():
    with app.app_context():
        while True:
            time.sleep(5)
            turbo.push(turbo.replace(render_template('load1min.html'), 'load1min'))
            turbo.push(turbo.replace(render_template('load5min.html'), 'load5min'))
            turbo.push(turbo.replace(render_template('load15min.html'), 'load15min'))
            turbo.push(turbo.replace(render_template('load30min.html'), 'load30min'))
            turbo.push(turbo.replace(render_template('load1hour.html'), 'load1hour'))
            turbo.push(turbo.replace(render_template('load4hour.html'), 'load4hour'))
            turbo.push(turbo.replace(render_template('loadpage1min.html'), 'pageload1min'))
            turbo.push(turbo.replace(render_template('loadpage5min.html'), 'pageload5min'))
            turbo.push(turbo.replace(render_template('loadpage15min.html'), 'pageload15min'))
            turbo.push(turbo.replace(render_template('loadpage30min.html'), 'pageload30min'))
            turbo.push(turbo.replace(render_template('loadpage1hour.html'), 'pageload1hour'))
            turbo.push(turbo.replace(render_template('loadpage4hour.html'), 'pageload4hour'))

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")