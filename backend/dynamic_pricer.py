import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from database.mongodb import db
from bson.objectid import ObjectId
from pandas import DataFrame
from sentiment_analysis.sentiment_analysis import sentiment_score_by_week
from math import ceil

sales_scaler = MinMaxScaler(feature_range=(0,1))
sales_scaler.fit(np.array([30,500]).reshape(-1,1))
loaded_model = load_model('./trained_models/dynamic_pricing/')
print('Loaded LSTM Model')

# input in the form:  pd.series / list of dict 
def scale_sales(data): 
    return pd.Series(sales_scaler.transform(data.values.reshape(-1,1)).flatten(), index=data.index)

def inverse_scale_sales(data):
    return pd.Series(sales_scaler.inverse_transform(data.values.reshape(-1,1)).flatten(), index=data.index)

def scale_price(data, range=[]):
    if len(range) == 0:
        min = data.min()
        max = data.max()
    else: 
        min = range[0]
        max = range[1]
    scaler = MinMaxScaler(feature_range=(0,1))
    scaler.fit(np.array([min,max]).reshape(-1,1))
    return pd.Series(scaler.transform(data.values.reshape(-1,1)).flatten(), index=data.index)

def inverse_scale_price(data, range):
    min = range[0]
    max = range[1]
    scaler = MinMaxScaler(feature_range=(0,1))
    scaler.fit(np.array([min,max]).reshape(-1,1))
    return pd.Series(scaler.inverse_transform(data.values.reshape(-1,1)).flatten(), index=data.index)

#input should be pandas Dataframe in the order: score, sales, price, Min Two rows
def predict_price(X, price_range):
    X['sales'] = scale_sales(X['sales'])
    X['price'] = scale_price(X['price'], price_range)
    actual_X = [[ X.iloc[-2].tolist(), X.iloc[-1].tolist() ]]
    result = loaded_model.predict(actual_X)
    actual_result = inverse_scale_price(pd.Series(result.flatten()), price_range)[0]
    return actual_result

def process_week(product_id):
    query = {"_id":ObjectId(product_id) }
    product = db['products'].find_one(query)
    sales = product['sales']
    week = len(sales)
    scores = product['scores']
    prices = product['prices']
    new_score = sentiment_score_by_week(product_id, week)
    scores.append(new_score)
    product['scores'] = scores
    if week < 2:
        product['recommended_price'] = prices[0]
    else:
        df = DataFrame({
            'score': scores,
            'sales': sales,
            'price': prices
        })
        new_price = predict_price(df, [product['min_price'], product['max_price']])
        product['recommended_price'] = ceil(new_price)
    db['products'].update_one(query, {'$set':  product})