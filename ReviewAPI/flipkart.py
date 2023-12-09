# -*- coding: utf-8 -*-
from math import ceil
from utilities import getHtml
import selectorlib
from dateutil.relativedelta import relativedelta
from datetime import date, datetime

flipkartReviewExtractor = selectorlib.Extractor.from_yaml_file('selectors/selectors_flipkart.yml')


def parseTime(raw):
    s = raw.split()
    if raw.lower() == 'today':
        d = date.today()
    elif len(s) == 3:

        if s[1].startswith("m"):
            d = date.today() - relativedelta(months = int(s[0]))
        if s[1].startswith("d"):
            d = date.today() - relativedelta(days = int(s[0]))
    else:
        d = datetime.strptime(raw, '%b, %Y')


    return d.strftime("%d-%m-%Y")

def parseFlipkartReview(raw):
    try: 
        reviews = []
        for review in raw['reviews']:
            if review['review_title'] == None:
                continue
            review['rating'] = float(review['rating'])
            review['likes'] = int(review['likes'].replace(",", ""))
            # review['dislikes'] = int(review['dislikes'].replace(",", ""))
            del review['dislikes']
            review['product_title'] = raw['product_title']
            review['average_rating'] = raw['average_rating']
            review['source'] = 'flipkart'
            review['price'] = raw['price'].replace('₹', '').replace(',','')
            review['time'] = parseTime(review['time'])
            reviews.append(review)
        return reviews
    except:
        return []

def getFlipkartReviews(url, details = False, no_of_reviews=50):
    htmlText = getHtml(url, mode="selenium", read_more_element_class='_1BWGvX')

    data = flipkartReviewExtractor.extract(htmlText,base_url=url)
    no_of_reviews = data['number_of_reviews'] = int(data['number_of_reviews'].split()[0].replace(",",""))
    print(no_of_reviews)
    no_of_pages = ceil(data['number_of_reviews'] / 10)

    histogram = {}
    for i in range(len(data['hist'])):
        histogram[data['hist'][i]] =int( data['val'][i].replace(",", ""))
    data['histogram'] = histogram
    data.pop("hist")
    data.pop("val")

    data['product_title'] = " ".join(data['product_title'].split(" ")[:-1])
    reviews = parseFlipkartReview(data)

    page = 2
    print("flipkart pages: 1", end = " ")
    while len(reviews) < no_of_reviews and page <= no_of_pages:
        htmlText = getHtml(url + "&page="+str(page), mode="selenium", read_more_element_class='_1BWGvX')
        print(page, end = " ")
        data1 = flipkartReviewExtractor.extract(htmlText,base_url=url)
        data1['product_title'] = data['product_title']
        reviews += parseFlipkartReview(data1)

        page += 1
    print()
    if details:
        data['reviews'] = reviews   
        return data

    return reviews


months = {	'Jan':'01',
		'Deb':'02',
		'Mar':'03',
		'Sep':'04',
		'May':'05',
		'JUN':'06',
		'JUL':'07',
		'AUG':'08',
		'SEPT':'09',
		'OCT':'10',
		'NOV':'11',
		'DEC':	'12'	}
