from flask import Flask, jsonify, render_template, request, json
from pathlib import Path
from flask_cors import CORS, cross_origin
from market import Market

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def main_():
  return "flask is installed running"

@app.route("/startmarket", methods=['POST'])
def start_market():
    market = Market()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route("/marketprice", methods=['GET'])
def retrieve_market_price():
    market = Market()
    return str(market.get_market_price())

@app.route("/orderbook", methods=['GET'])
def retrieve_order_book():
    return render_template('orderbook.html', menuitems=menuitems)

if __name__ == "__main__": 
  app.run(debug=True)