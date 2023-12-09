# This is used for scraping the products and Reviews given a keyword. Reuslt is stored in CSV form in a filename given.
# This is the script used for getting dataset for dynamic pricing

import selectorlib
from utilities import getHtml
from laptop import getModelNumber

from flipkart import *
from amazon import *
import pandas as pd
import sys

yaml_string = '''
    title:
        product_title:
        css: 'span.B_NuCI'
        type: Text
    '''

flipkartProductExtractor =  selectorlib.Extractor.from_yaml_file('selectors/flipkartProductSelector.yml')
flipkartProductExtractorAlternative =  selectorlib.Extractor.from_yaml_file('selectors/flipkartProduct_Alternate.yml')
amazonProductExtractor = selectorlib.Extractor.from_yaml_file('selectors/amazonProductSelector.yml')
flipkartTitleSelector = selectorlib.Extractor.from_yaml_string(yaml_string)

def getProductsandReviews(query):
    try:
        productsFlipkart = []
        for i in range(1,2):
            flipkartQueryUrl ="https://www.flipkart.com/search?q=" + query.replace(" ", "%20") + "&page="+str(i)
            htmlText = getHtml(flipkartQueryUrl)
            try: 
                productsFlipkart += flipkartProductExtractor.extract(htmlText,base_url="https://flipkart.com")["products"][0:11]
            except:
                productsFlipkart += flipkartProductExtractorAlternative.extract(htmlText,base_url="https://flipkart.com")["products"][0:11]
                
        for product in productsFlipkart:
            if product["title"].endswith("..."):
                res = flipkartTitleSelector.extract(getHtml(product["url"]))
                title = res['title']
                product["title"] = title

        new_product_list = []
        reference = []
        for i in range(len(productsFlipkart)):
            if productsFlipkart[i]['ad'] == None:
                cur = productsFlipkart[i]['title'].split('(')[0]
                if cur not in reference:
                    reference.append(cur)
                    new_product_list.append(productsFlipkart[i])

        productsFlipkart = new_product_list
        productsAmazon = []

        for product in productsFlipkart:
            model = getModelNumber(product["title"])
            amazonQueryUrl = "https://www.amazon.in/s?k=" + model.replace(" ", "+") + "&rh=n%3A1805560031%2Cp_n_condition-type%3A8609960031"
            html = getHtml(amazonQueryUrl)
            # with open('temp.html', 'w' ) as w :
            #     w.write(html)
            temp = amazonProductExtractor.extract(html, base_url="https://amazon.in")
            i = 1
            while temp['products'] == None:
                i+=1
                print(i, end = " ")
                html = getHtml(amazonQueryUrl)
                temp = amazonProductExtractor.extract(html, base_url="https://amazon.in")
            print()
            amazonProduct = temp['products'][0]
            productsAmazon.append(amazonProduct)
        reviews = []
        for index, product in enumerate(productsFlipkart):
            l = product["url"].split('/')
            temp = l[5].split('&')
            urlf = "https://flipkart.com/"+l[3]+"/product-reviews/"+temp[0]+"&"+temp[1]+'&marketplace=FLIPKART'
            chunks = productsAmazon[index]['url'].split("/")
            if chunks[3] != 'dp':

                urla = "https://amazon.in/" +  chunks[3] +"/product-reviews/" + chunks[5]
            else:
                urla = "https://amazon.in" +"/product-reviews/" + chunks[4]+'/'+chunks[5]

            reviewst = getFlipkartReviews(urlf,False, 50)
            reviewst += getAmazonReviews(urla,False, 50)

            for i in reviewst:
                i['id'] = index

            reviews += reviewst
        print(len(reviews))
        pd.DataFrame.from_dict(reviews).to_csv('scraped_datasets_new/'+sys.argv[2], index= False)
    except Exception as e:
        with open('exception2.html', 'w') as w:
            w.write(htmlText)
        raise e

getProductsandReviews(sys.argv[1],1)

