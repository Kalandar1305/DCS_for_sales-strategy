import selectorlib
from amazon import getAmazonReviews
from utilities import getHtml
from flipkart import *
import pandas
flipkartProductExtractor =  selectorlib.Extractor.from_yaml_file('selectors/flipkartProductSelector.yml')
amazonProductExtractor = selectorlib.Extractor.from_yaml_file('selectors/amazonProductSelector.yml')

def queryFlipkart(query, no_of_products, no_of_reviews_per_product):
    queryUrl ="https://www.flipkart.com/search?q=" + query.replace(" ", "%20")

    htmlText = getHtml(queryUrl)

    data = flipkartProductExtractor.extract(htmlText,base_url=queryUrl)

    page = 2

    while(len(data['products']) < no_of_products):
        s = flipkartProductExtractor.extract(getHtml(queryUrl+"&page="+str(page)), base_url=queryUrl)['products']
        data['products'] += s
        page += 1

    urls = []

    for link in data['products'][:no_of_products]:
        l = link["url"].split('/')
        temp = l[5].split('&')
        urls.append("https://flipkart.com/"+l[3]+"/product-reviews/"+temp[0]+"&"+temp[1]+'&marketplace=FLIPKART')

    reviews = []
    for l in range(no_of_products):
        reviews += (getFlipkartReviews(urls[l],no_of_reviews=no_of_reviews_per_product))
    
    return reviews

def queryAmazon(query, no_of_products, no_of_reviews_per_product):

    getMode = ""
    page = 2
    urls = []
    reviews = []

    queryUrl = "https://www.amazon.in/s?k=" + query.replace(" ", "+")
    html = getHtml(queryUrl,mode=getMode)


    data = amazonProductExtractor.extract(html)

    if data['products'] == None:
        getMode = 'selenium'
        html = getHtml(queryUrl, mode=getMode)
        data = amazonProductExtractor.extract(html)
        urls += data["products"]

    while len(urls) < no_of_products: 
        try:
            html = getHtml(queryUrl+"&page="+str(page), mode=getMode)
            data = amazonProductExtractor.extract(html)
            urls += data["products"]

            page += 1
        except:
            pass

    for url in urls[:no_of_products]:
        chunks = url["url"].split("/")
        review_url = "https://amazon.in/" +  chunks[1] +"/product-reviews/" + chunks[3]
        reviews += getAmazonReviews(review_url, no_of_reviews=no_of_reviews_per_product)

    return reviews


if __name__ == '__main__':
    query = input("Enter query: ")
    no_of_products = int(input("Enter no of products: "))
    no_of_reviews_per_product = int(input("Enter Number of reviews per product: "))

    reviews = []
    reviews += queryFlipkart(query, no_of_products, no_of_reviews_per_product)
    reviews += queryAmazon(query,no_of_products, no_of_reviews_per_product)
    df = pandas.DataFrame(reviews)
    df.to_csv("result.csv",index=False,columns=["source","product_title","average_rating","review_title","content","rating","likes"])