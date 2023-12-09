import selectorlib
from web_scrape.utilities import getHtml
from web_scrape.laptop import getModelNumber
from web_scrape.specifications import get_specifications

yaml_string = '''
    title:
        product_title:
        css: 'span.B_NuCI'
        type: Text
    '''
flipkartProductExtractor =  selectorlib.Extractor.from_yaml_file('web_scrape/selectors/flipkartProductSelector.yml')
flipkartProductExtractorAlternative =  selectorlib.Extractor.from_yaml_file('web_scrape/selectors/flipkartProduct_Alternate.yml')
amazonProductExtractor = selectorlib.Extractor.from_yaml_file('web_scrape/selectors/amazonProductSelector.yml')
flipkartTitleSelector = selectorlib.Extractor.from_yaml_string(yaml_string)

def get_competitor_products(product_i):
    search_string = ""
    if 'processor' in product_i['specifications']:
        search_string +=  product_i['specifications']['processor']
    if "graphics" in product_i['specifications']:
        search_string += " " +  product_i['specifications']['graphics']
    if "RAM" in product_i['specifications']:
        search_string += " " +  product_i['specifications']['RAM']
    if "storage" in product_i['specifications']:
        search_string += " " +  product_i['specifications']['storage']
    
    try:
        productsFlipkart = []
        for i in range(1,2):
            flipkartQueryUrl ="https://www.flipkart.com/search?q=" + search_string.replace(" ", "%20")+"&page="+str(i)
            htmlText = getHtml(flipkartQueryUrl)
            try: 
                productsFlipkart += flipkartProductExtractor.extract(htmlText,base_url="https://flipkart.com")["products"][0:5]
            except:
                productsFlipkart += flipkartProductExtractorAlternative.extract(htmlText,base_url="https://flipkart.com")["products"][0:5]
                
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
            product['price'] = int(product['price'].replace("₹", '').replace(',', ''))
            brand = product['title'].split()[0].lower()
            part = None
            if brand.lower() == 'realme':
                continue
            if brand == 'lenovo': 
                specifications = get_specifications(product['url'])
                if 'Part Number' in specifications:
                    part = specifications['Part Number']
            model, matched = getModelNumber(product["title"], part = part)
            
            amazonQueryUrl = "https://www.amazon.in/s?k=" + model.replace(" ", "+") + "&rh=n%3A1805560031%2Cp_n_condition-type%3A8609960031"
            html = getHtml(amazonQueryUrl)
            # with open('temp.html', 'w' ) as w :
            #     w.write(html)
            temp = amazonProductExtractor.extract(html, base_url="https://amazon.in")
            i = 1
            while temp['products'] == None:
                i+=1
                print(i, end = " ")
                html = getHtml(amazonQueryUrl, mode =  "" if i%2==0 else 'selenium')
                temp = amazonProductExtractor.extract(html, base_url="https://amazon.in")
            if i>1:
                print()
            amazonProduct = temp['products'][0]

            model2, matched = getModelNumber(amazonProduct['title'])

            if matched:
                if model.replace(" ", '') == model2.replace(' ',''):
                    productsAmazon.append(amazonProduct)
                else:
                    productsAmazon.append(None)
            else:
                if product_i['type'] == 'mobile':
                    productsAmazon.append(amazonProduct)
                else:
                    productsAmazon.append(None)
        overall = []
        for i in range(len(productsAmazon)):
            f = productsFlipkart[i]
            a = productsAmazon[i]

            if a:
                a['price'] = int(a['price'].replace("₹", '').replace(',', ''))
            try:
                f_n_ratings = float(f['n_ratings'].split()[0].replace(",", '').replace("(", "").replace(")", ""))
            except:
                f_n_ratings = 0
            try:
                a_n_ratings = float(a['n_ratings'].split()[0].replace(",", ''))
            except: 
                a_n_ratings = 0
            try: 
                f_rating = float(f['rating'])
            except:
                f_rating = 0
            try: 
                
                a_rating = float(a['rating'].split()[0])
            except:
                a_rating = 0

            if f_n_ratings <10 and a_n_ratings < 10:
                continue
            avgRating = ( f_n_ratings *  f_rating + a_n_ratings * a_rating) / ( f_n_ratings +  a_n_ratings )
            temp = {
                'title' : f["title"],
                'flipkartUrl': f['url'],
                'amazonUrl': a['url'] if a else None,
                'flipkartRating': f_rating,
                'amazonRating':a_rating if a else None,
                'averageRating': avgRating,
                'amazonPrice': a['price'],
                'flipkartPrice': f['price'],
                "model":model
            }
            f = True
            for i in overall:
                if i['model'] == model:
                    f = False
                    break
            if f:
                temp['specifications'] = get_specifications(temp['flipkartUrl'], product_i['type'])

                overall.append(temp)
        overall.sort(key=lambda x: x["averageRating"], reverse=True)
        
        return overall
    except Exception as e:
        with open('exception2.html', 'w') as w:
            w.write(htmlText)
        raise e