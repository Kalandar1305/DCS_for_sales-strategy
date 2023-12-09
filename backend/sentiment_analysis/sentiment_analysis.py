from database.mongodb import db
from pandas import date_range, DataFrame,to_datetime, concat
from joblib import load

tfidf_vectorizer = load('./trained_models/TVEC.joblib')
sentiment_analyser = load('trained_models/RF.joblib')


def get_sentiment(df:DataFrame):
    sparse_matrix = tfidf_vectorizer.transform(df['content'])
    df['sentiment'] = sentiment_analyser.predict(sparse_matrix)

    return df
def get_reviews_by_week(product_id, week):
    query = {"product_id": product_id}
    reviews = db['reviews'].find_one(query)['reviews']
    reviews = DataFrame.from_dict(reviews)
    reviews['time'] = to_datetime(reviews['time'], format='%d-%m-%Y')
    reviews = reviews.sort_values("time").reset_index()
    date_ranges = date_range(
            start=reviews["time"].min(), end=reviews["time"].max(), freq="7D"
        )
    # i = week-1
    # if len(date_ranges) >=i:
    #     start_date = date_ranges[i]
    #     end_date = date_ranges[i + 1]
    #     week_reviews = reviews[
    #         (reviews["time"] >= start_date) & (reviews["time"] < end_date)
    #     ]
    #     return week_reviews
    for i in range(len(date_ranges) - 1):
        start_date = date_ranges[i]
        end_date = date_ranges[i + 1]
        
        temp = reviews[
            (reviews["time"] >= start_date) & (reviews["time"] < end_date)
        ]

    week_groups = []
    count = 0
    for i in range(len(date_ranges) - 1):
        start_date = date_ranges[i]
        end_date = date_ranges[i + 1]
        
        temp = reviews[
            (reviews["time"] >= start_date) & (reviews["time"] < end_date)
        ]
        if len(temp) != 0:
            count += 1
        week_groups.append(temp)
        if count == week:
            break
    new_df = concat(week_groups).reset_index()

    return new_df

def get_sentiment_score(df:DataFrame):
    # df.reset_index(inplace=True)
    df['likes'].fillna(0, inplace=True)
    df['helpful'] = df['likes'].apply(lambda n: n+1)
    sum = df['helpful'].sum()

    result = {
        0: 0,
        1: 0,
        2: 0
    }

    for index, sentiment  in enumerate(df['sentiment']):
        result[sentiment] += df['helpful'][index]

    score = (-1 * result[0] + 1*result[2]) / sum
        
    return score

def sentiment_score_by_week(product_id, week):
    reviews = get_reviews_by_week(product_id, week)
    
    query = { "product_id" : product_id }
    d  = db['reviews'].find_one(query)
    d['actual_reviews'] = reviews.to_dict('records')
    set = {"$set": d}
    db['reviews'].update_one(query, set)
    # reviews_classified = get_sentiment(reviews)
    score = get_sentiment_score(reviews)
    return score

