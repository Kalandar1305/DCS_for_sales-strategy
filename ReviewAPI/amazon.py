from math import ceil
import selectorlib
from utilities import getHtml
extractorAmazon =  selectorlib.Extractor.from_yaml_file('selectors/selectors_amazon.yml')
def parseTime(raw):
    s = raw.split()[-3:]

    return s[0].zfill(2) + "-"+ months[s[1].lower()] +"-" + s[2]

def parseAmazonReview(raw):
    try: 
        reviews = []
        for r in raw['reviews']:
            likes = r['likes'].split()[0] if r['likes'] != None else 0
            r['likes'] = int('1' if likes == 'One' else likes)
            r['rating'] = float(r['rating'].split(' out of')[0])
            r['product_title'] = raw['product_title']
            r['average_rating'] = raw['average_rating']
            r['source'] = 'amazon'
            r['price'] = 0
            r['time'] = parseTime(r['time'])
            reviews.append(r)
        return reviews
    except:
        return []

def getAmazonReviews(url, details = False, no_of_reviews=50):
    try:
        htmlText = getHtml(url, mode='')

        data = extractorAmazon.extract(htmlText,base_url=url)

        data['average_rating'] = float(data['average_rating'].split(' out')[0])
        no_of_reviews = data['number_of_reviews'] = int(data['number_of_reviews'].split()[3].replace(",",""))
        print(no_of_reviews)
        if no_of_reviews > 0:
            reviews = parseAmazonReview(data)
            histogram = {}
            for i in data['histogram']:
                if i['key'] != None and i['value'] != None:
                    histogram[i['key'].split()[0]] = int((int(i['value'].replace("%",""))/100)*data['number_of_reviews'])
            data['histogram'] = histogram
            num_of_pages = min(ceil(data['number_of_reviews']/10), ceil(no_of_reviews/10))
            skipcount = 0
            print("amazon pages: 1", end = " ")
            for i in range(2, num_of_pages):
                print(i, end = " ")
                htmlText = getHtml(url + "/ref=cm_cr_getr_d_paging_btm_next_"+str(i)+"?pageNumber="+str(i))
                data1 = extractorAmazon.extract(htmlText, base_url=url)
                data1['average_rating'] = data['average_rating']
                parsedReviews =  parseAmazonReview(data1) 
                if len(parsedReviews) == 0:
                    if skipcount == 5:
                        print("page: ", i, ' skipped')
                        break
                    skipcount += 1
                reviews += parsedReviews
            print()
            data['reviews'] = reviews
            if details:
                return data
        
            return reviews
            
        if details:
            return data
        
        return []

    except Exception as e:
        with open('exception.html', 'w') as w:
            w.write(htmlText)
        print(url)
        raise e

months = {	'january':'01',
		'february':'02',
		'march':'03',
		'april':'04',
		'may':'05',
		'june':'06',
		'july':'07',
		'august':'08',
		'september':'09',
		'october':'10',
		'november':'11',
		'december':	'12'	}