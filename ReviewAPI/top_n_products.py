import selectorlib
from utilities import getHtml
from laptop import getModelNumber
import json

yaml_string = '''
    title:
        product_title:
        css: 'span.B_NuCI'
        type: Text
    '''

flipkartProductExtractor =  selectorlib.Extractor.from_yaml_file('selectors/flipkartProductSelector.yml')
amazonProductExtractor = selectorlib.Extractor.from_yaml_file('selectors/amazonProductSelector.yml')
flipkartTitleSelector = selectorlib.Extractor.from_yaml_string(yaml_string)

def getProducts(query):
    flipkartQueryUrl ="https://www.flipkart.com/search?q=" + query.replace(" ", "%20")
    htmlText = getHtml(flipkartQueryUrl)
    productsFlipkart = flipkartProductExtractor.extract(htmlText,base_url="https://flipkart.com")["products"][2:11]

    for product in productsFlipkart:
        if product["title"].endswith("..."):
            res = flipkartTitleSelector.extract(getHtml(product["url"]))
            title = res['title']
            product["title"] = title

    productsAmazon = []

    for product in productsFlipkart:
        product["rating"] = float(product['rating'])
        product['n_ratings'] = int(product['n_ratings'].split()[0].replace(",",""))
        model = getModelNumber(product["title"])
        amazonQueryUrl = "https://www.amazon.in/s?k=" + model.replace(" ", "+")
        html = getHtml(amazonQueryUrl)
        temp = amazonProductExtractor.extract(html, base_url="https://amazon.in")["products"]
        amazonProduct = temp[0]
        try:

            amazonProduct['n_ratings'] = int(amazonProduct['n_ratings'].split()[0].replace(",",""))
            amazonProduct['rating'] = float(amazonProduct['rating'].replace("(","").replace(")",""))
        except:
            amazonProduct['rating'] = 0
            amazonProduct['n_ratings'] = 0
            
        productsAmazon.append(amazonProduct)


    # print(productsAmazon)

    # print(productsFlipkart)

    overall = []

    for i in range(len(productsAmazon)):
        f = productsFlipkart[i]
        a = productsAmazon[i]

        avgRating = ( f['n_ratings'] *  f["rating"] + a["n_ratings"] * a["rating"]) / ( f["n_ratings"] +  a["n_ratings"] )

        temp = {
            'title' : f["title"],
            'flipkartUrl': f['url'],
            'amazonUrl': a['url'],
            'flipkartRating': f['rating'],
            'amazonRating':a['rating'],
            'averageRating': avgRating
        }

        overall.append(temp)


        overall.sort(key=lambda x: x["averageRating"], reverse=True)

        print(overall)

        with open("result.json", "w") as f:
            f.write(json.dumps(overall))

getProducts("laptops",1)

