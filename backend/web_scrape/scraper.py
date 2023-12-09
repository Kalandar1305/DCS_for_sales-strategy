from web_scrape.amazon import getAmazonReviews
from web_scrape.flipkart import getFlipkartReviews
from pandas import DataFrame
from database.mongodb import db

from sentiment_analysis.sentiment_analysis import get_sentiment

def scrape_reviews(flipkartURL, amazonURL, id):
    l = flipkartURL.split('/')
    temp = l[5].split('&')
    reviewURLf = "https://flipkart.com/"+l[3]+"/product-reviews/"+temp[0]+"&"+temp[1]+'&marketplace=FLIPKART'
    chunks = amazonURL.split("/")
    if chunks[3] != 'dp':
        reviewURLa = "https://amazon.in/" +  chunks[3] +"/product-reviews/" + chunks[5]
    else:
        reviewURLa = "https://amazon.in" +"/product-reviews/" + chunks[4]+'/'+chunks[5]
    
    reviewsA = getAmazonReviews(reviewURLa)
    reviewsF = getFlipkartReviews(reviewURLf)
    for review in reviewsA:
        review['price'] = reviewsF[0]['price']
    reviews = reviewsF + reviewsA
    df = DataFrame.from_dict(reviews)
    reviews = get_sentiment(df).to_dict('records')
    data = {
        'product_id': id,
        'reviews' : reviews,
        'actual_reviews': []
    }
    result = db['reviews'].insert_one(data)

    return result.inserted_id

def scrape_specification(flipkartURL, type):
    if type == 'laptop': 

        pass
    if type == 'mobile':
        
        pass