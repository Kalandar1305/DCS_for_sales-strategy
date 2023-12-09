from bson.objectid import ObjectId
from flask import Flask, request, jsonify, send_file, Response
from threading import Thread
from database.mongodb import db
from sentiment_analysis.tokenizer import customTokenizer
from web_scrape.scraper import scrape_reviews
from bson.objectid import ObjectId
from dynamic_pricer import process_week
from graph import generate_bar_graph, generate_line_graph,generate_aspect_graph
from flask_cors import CORS
from web_scrape.specifications import get_specifications
from web_scrape.competitor_products import get_competitor_products
from sentiment_analysis.aspect_sentiment_analysis import get_aspect_sentiment
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    data['sales'] = []
    data['scores'] = []
    data['prices'] = [int(data['price']),]
    data['recommended_price'] = None
    fURL = data['urls']['flipkartURL']
    data['specifications'] = get_specifications(fURL, data['type'])
    inserted = db['products'].insert_one(data)
    if '_id' in data:
        del data['_id']
    data['id'] = str(inserted.inserted_id)
    data['status'] = 0
    Thread(target=process_post_add_product, args=(data, str(inserted.inserted_id))).start()
    return jsonify(data)


@app.route('/get_products', methods=['GET'])
def get_products():
    data = []
    for document in db['products'].find():
        document['id'] = str(document['_id'])
        del document['_id']
        data.append(document)
    return jsonify(data)


@app.route('/add_sales', methods=['POST'])
def add_sales():
    data = request.get_json()
    query = {'_id': ObjectId(data['id'])}
    existing_data = db['products'].find_one(query)
    sales = existing_data['sales']
    sales.append(data['sales'])
    new_value = {'$set': {'sales': sales}}
    db['products'].update_one(query, new_value)
    thread = Thread(target=process_week, args=(data['id'],))
    thread.start()
    return 'Inserted'


@app.route('/get_predicted_price/<product_id>', methods=['GET'])
def get_predicted_price(product_id):
    query = {'_id': ObjectId(product_id)}
    price = db['products'].find_one(query)['recommended_price']
    query2 = {'product_id': product_id}
    cp = db['competitive_products'].find_one(query2)
    
    if price != None:
        return jsonify(
        {
            "price": price,
            # "cp": [ { "title": i['title'], 'amazonPrice': i['amazonPrice'], 'flipkartPrice':i['flipkartPrice'] } for i in cp['products']    ]
        }
        )
    else:
        return Response("Not available right Now. Please visit after some time.", status=400)


@app.route('/set_price', methods=['POST'])
def set_price():
    data = request.get_json()
    query = {'_id': ObjectId(data['product_id'])}
    product = db['products'].find_one(query)
    product['price'] = data['price']
    product['prices'].append(data['price'])
    product['recommended_price'] = None
    db['products'].update_one(query, {"$set": product})
    return "Done"


@app.route('/negative_reviews/<product_id>', methods=['GET'])
def get_negative_reviews(product_id):
    query = {"product_id": product_id}
    reviews = db['reviews'].find_one(query)
    neg_reviews = []
    for review in reviews['actual_reviews']:
        if review['sentiment'] == 0:
            neg_reviews.append(
                {"title": review['review_title'], "content": review['content']})
    return jsonify(neg_reviews)


@app.route('/positive_reviews/<product_id>', methods=['GET'])
def get_positive_reviews(product_id):
    query = {"product_id": product_id}
    reviews = db['reviews'].find_one(query)
    neg_reviews = []
    for review in reviews['actual_reviews']:
        if review['sentiment'] == 1 or review['sentiment'] == 2:
            neg_reviews.append(
                {"title": review['review_title'], "content": review['content']})
    return jsonify(neg_reviews)


@app.route('/polarity_bar_chart/<product_id>', methods=['GET'])
def polarity_bar_chart(product_id):
    numbers = {
        0: 0,
        1: 0,
        2: 0
    }

    query = {"product_id": product_id}
    reviews = db['reviews'].find_one(query)['reviews']
    for review in reviews:
        numbers[review['sentiment']] += 1

    count = {
        'positive': numbers[2],
        'neutral': numbers[1],
        'negative': numbers[0]
    }

    return jsonify({
        "product_id": product_id,
        "path": generate_bar_graph(count)
    })


@app.route('/graphs/<product_id>', methods=['GET'])
def week_sales_line_graph(product_id):
    query = {"_id": ObjectId(product_id)}
    product = db['products'].find_one(query)
    sales = {}
    scores = {}
    for index, i in enumerate(product['sales']):
        sales['Week ' + str(index+1)] = i
        scores["Week " + str(index+1)] = product['scores'][index]

    numbers = {
        0: 0,
        1: 0,
        2: 0}

    query = {"product_id": product_id}
    reviews = db['reviews'].find_one(query)['actual_reviews']
    for review in reviews:
        numbers[review['sentiment']] += 1

    count = {
        'positive': numbers[2],
        'neutral': numbers[1],
        'negative': numbers[0]
    }

    return jsonify({
        "product_id": product_id,
        "image2": generate_line_graph(sales, scores),
        "image1": generate_bar_graph(count)
    })

@app.route('/competitive_products/<product_id>', methods=['GET'])
def get_competitive_products(product_id):
    query = {'product_id': product_id}
    result = db['competitive_products'].find_one(query)
    del result['_id']
    for product in result['products']:
        product['company'] = product['title'].split()[0]
    return jsonify(result)

@app.route('/delete-product/<id>', methods=['DELETE'])
def delete_product(id):
    query = { '_id': ObjectId(id) }
    db['products'].delete_one(query)
    query = {'product_id': id}
    db['competitive_products'].delete_one(query)
    db['reviews'].delete_one(query)

    return jsonify({ 'message': 'success'})

@app.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    try:
        return send_file(f'images/{filename}', mimetype='image/png')
    except Exception as e:
        return str(e)

@app.route('/aspect-sentiment/<id>', methods=['GET'])
def aspect_sentiment(id):
    query = {'product_id': id}
    reviews = db['reviews'].find_one(query)['reviews']

    sentiment = get_aspect_sentiment(reviews)
    images = generate_aspect_graph(sentiment)
    return jsonify({"images": images})

def process_post_add_product(data, inserted_id):
    fURL = data['urls']['flipkartURL']
    aURL = data['urls']['amazonURL']
    scrape_reviews(fURL, aURL, inserted_id)
    result = get_competitor_products(data)
    query = {
        'product_id' : inserted_id,
        'products' : result
    }

    db['competitive_products'].insert_one(query)
    db['products'].update_one({ '_id': ObjectId(inserted_id) }, {"$set": { 'status': 1 }})
    print('Product', inserted_id, 'Processed')


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=False)
# app.run(host="0.0.0.0", debug=False)
