from flask import Flask, request, jsonify
from flask_cors import CORS
from amazon import *
from flipkart import *
from query import *

app = Flask(__name__)
app.debug = True
CORS(app,resources={r"/*": {"origins": "*"}})

@app.route("/flipkart")
def flipkart():
    url = request.args.get('url',None)
    pages = True if request.args.get('pages',None) else False
    details = True if request.args.get('details',None) else False
    if url:
        data = getFlipkartReviews(url,pages, details)
        return jsonify(data)
    return jsonify({'error':'URL to scrape is not provided'}),400

@app.route("/amazon")
def amazon():
    pages = True if request.args.get('pages',None) else False
    details = True if request.args.get('details',None) else False
    url = request.args.get('url',None)
    if url:
        data = getAmazonReviews(url, pages, details)
        return jsonify(data)
    return jsonify({'error':'URL to scrape is not provided'}),400

@app.route("/")
def get():
    query = request.args.get('q',None)
    no_of_products = int(request.args.get('no_of_products',None))
    no_of_reviews_per_product = int(request.args.get('no_of_reviews_per_product',None))
    reviews = queryAmazon(query, no_of_products, no_of_reviews_per_product)
    reviews += queryFlipkart(query, no_of_products, no_of_reviews_per_product)
    return jsonify(reviews)

if __name__ == "__main__":
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5000)

    app.run(host = "0.0.0.0", port= 5000, debug=True)
