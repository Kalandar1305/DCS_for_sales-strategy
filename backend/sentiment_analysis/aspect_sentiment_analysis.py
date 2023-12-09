from sentiment_analysis.tokenizer import customTokenizer
from sentiment_analysis.sentiment_analysis import get_sentiment
from pandas import DataFrame

def get_aspect_sentiment(reviews):
    aspects = ['battery', 'camera', 'performance', 'display', 'graphics', 'processor']
    aspect_dict = {
        'battery': [],
        'camera': [],
        'performance': [],
        'display': [],
        'graphics':[],
        'processor': []
    }
    aspect_sentiment = {
    'battery': [],
    'camera': [],
    'performance': [],
    'display': []
    }
    for review in reviews: 
        for sentance in review['content'].split('.'):
            for aspect in aspects:
                if aspect in sentance.lower():
                    aspect_dict[aspect].append(sentance)
    for aspect in aspects:
        aspect_dict[aspect] = DataFrame(aspect_dict[aspect], columns = ['content'])
    for aspect in aspects:
        positive = negative = neutral = 0
        if len(aspect_dict[aspect]) > 0:
            res = get_sentiment(aspect_dict[aspect])
            positive = len(res[res['sentiment'] == 2])
            neutral = len(res[res['sentiment'] == 1])
            negative = len(res[res['sentiment'] == 0])
        aspect_sentiment[aspect] = [positive, neutral, negative]
    p1 = aspect_sentiment['processor']
    p2 = aspect_sentiment['performance']
    aspect_sentiment['performance'] = [ p1[0] + p2[0], p1[1] + p2[1], p1[2]+p2[2] ]
    del aspect_sentiment['processor']
    return aspect_sentiment