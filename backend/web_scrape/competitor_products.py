import selectorlib
from web_scrape.utilities import getHtml
from web_scrape.laptop import getModelNumber
from web_scrape.specifications import get_specifications
flipkart_details = '''
    title:
        css: 'span.B_NuCI'
        type: Text
    rating:
        css: 'div._3LWZlK'
        type: Text
    n_ratings: 
        css: 'span._2_R_DZ'
        type: Text
'''
amazon_details = '''
    title:
        css: 'span.B_NuCI'
        type: Text
    rating:
        css: 'div.centerColAlign a.a-popover-trigger span.a-size-base'
        type: Text
    n_ratings: 
        css: 'div.centerColAlign span.a-declarative a.a-link-normal span.a-size-base'
        type: Text
'''
flipkartProductExtractor =  selectorlib.Extractor.from_yaml_file('web_scrape/selectors/flipkartProductSelector.yml')
flipkartProductExtractorAlternative =  selectorlib.Extractor.from_yaml_file('web_scrape/selectors/flipkartProduct_Alternate.yml')
amazonProductExtractor = selectorlib.Extractor.from_yaml_file('web_scrape/selectors/amazonProductSelector.yml')
flipkartTitleSelector = selectorlib.Extractor.from_yaml_string(flipkart_details)
amazonDetailsSelector = selectorlib.Extractor.from_yaml_string(amazon_details)
def get_average_rating(a, f):
            if a and a['price']:
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
            flag = True # Product contains enough reviews, So it can be added
            if f_n_ratings <10 and a_n_ratings < 10:
                 flag = False # Product Should not be added.
            if not flag:
                 return  {"f": 0, "a": 0, "avg": 0}, False
            avgRating = ( f_n_ratings *  f_rating + a_n_ratings * a_rating) / ( f_n_ratings +  a_n_ratings )


            return {"f": f_rating, "a": a_rating, "avg": avgRating}, flag
def unique_flipkart_product(productsFlipkart):
    new_product_list = []
    reference = []
    for i in range(len(productsFlipkart)):
        if productsFlipkart[i]['ad'] == None:
            cur = productsFlipkart[i]['title'].split('(')[0]
            if cur not in reference:
                reference.append(cur)
                new_product_list.append(productsFlipkart[i])
    return new_product_list
def get_flipkart_products(search_string):
    productsFlipkart = []
    for i in range(1,2):
        flipkartQueryUrl ="https://www.flipkart.com/search?q=" + search_string.replace(" ", "%20")+"&page="+str(i)
        htmlText = getHtml(flipkartQueryUrl)
        try: 
            productsFlipkart += flipkartProductExtractor.extract(htmlText,base_url="https://flipkart.com")["products"][0:11]
        except:
            productsFlipkart += flipkartProductExtractorAlternative.extract(htmlText,base_url="https://flipkart.com")["products"][0:11]
            
    for product in productsFlipkart:
        product['price'] = int(product['price'].replace("₹", '').replace(',', ''))
        productHTML = getHtml(product["url"])
        res = flipkartTitleSelector.extract(productHTML)
        while res['title'] == None and res['rating'] == None  and res['n_ratings'] == None:
            productHTML = getHtml(product["url"])
            res = flipkartTitleSelector.extract(productHTML)
        product['specifications'] = get_specifications(product['url'], search_string.split()[0])
        product["title"] = res['title']
        product['rating'] = res['rating']
        product['n_ratings'] = res['n_ratings']
            
    return unique_flipkart_product(productsFlipkart)
def get_amazon_price_by_fproducts_list(productsFlipkart, type):
        productsAmazon = []
        delete_flipkart_items = []
        for index, product in enumerate(productsFlipkart):
            brand = product['title'].split()[0].lower()
            part = None
            if brand == 'realme' and type == 'laptop':
                delete_flipkart_items.append(index)
                continue
            if brand == 'lenovo' and type == 'laptop': 
                specifications = get_specifications(product['url'],type)
                if 'Part Number' in specifications:
                    part = specifications['Part Number']
            model, matched = getModelNumber(product["title"], part = part)

            product['model'] = model

            amazonQueryUrl = "https://www.amazon.in/s?k=" + model.replace(" ", "+") + "&rh=n%3A1805560031%2Cp_n_condition-type%3A8609960031"
            html = getHtml(amazonQueryUrl)
            temp = amazonProductExtractor.extract(html, base_url="https://amazon.in")

            i = 1
            while temp['products'] == None:
                i+=1
                print(i, end = " ")
                html = getHtml(amazonQueryUrl, mode =  "" if i%2==0 else 'selenium')
                temp = amazonProductExtractor.extract(html, base_url="https://amazon.in")

            amazonProduct = temp['products'][0]

            model2, matched = getModelNumber(amazonProduct['title'])
            
            is_model_same = model.replace(" ", '') == model2.replace(' ','')

            if (matched and is_model_same) or ((not matched) and type == 'mobile'):
                if amazonProduct['rating'] == None or amazonProduct['n_ratings'] == None:
                    html = getHtml(amazonProduct['url'])
                    res = amazonDetailsSelector.extract(html)
                    amazonProduct['rating'] = res['rating']
                    amazonProduct['n_ratings'] = res['n_ratings']
                productsAmazon.append(amazonProduct)

            else:
                productsAmazon.append(None)

            # if matched:
            #     if is_model_same:
            #         productsAmazon.append(amazonProduct)
            #     else:
            #         productsAmazon.append(None)
            # else:
            #     if type == 'mobile':
            #         productsAmazon.append(amazonProduct)
            #     else:
            #         productsAmazon.append(None)
        print()

        productsFlipkart = [product for index, product in enumerate(productsFlipkart) if index not in delete_flipkart_items]

        return productsFlipkart, productsAmazon
def get_overall_products(productsAmazon, productsFlipkart, type):
        overall = []
        models = []

        for i in range(len(productsAmazon)):
            f = productsFlipkart[i]
            a = productsAmazon[i]
            res, flag = get_average_rating(a,f)

            if not flag:
                continue
            
            temp = {
                'title' : f["title"],
                'flipkartUrl': f['url'],
                'amazonUrl': a['url'] if a else None,
                'flipkartRating': res['f'],
                'amazonRating':res['a'] if a else None,
                'averageRating': res['avg'],
                'amazonPrice': a['price'] if a else None,
                'flipkartPrice': f['price'],
                "model":f['model'] if 'model' in f else None,
                'specifications': f['specifications'] if 'specifications' in f else get_specifications(f['url'], type)
            }

            models.append(f['model'])
            f = True
            if['model'] not in models:
                overall.append(temp)

        overall.sort(key=lambda x: x["averageRating"], reverse=True)
        return overall  
def get_search_string(product_i):
    search_string = product_i['type'] + " "
    if 'processor' in product_i['specifications'] :
        search_string +=  product_i['specifications']['processor']
    if "graphics" in product_i['specifications']:
        search_string += " " +  product_i['specifications']['graphics']
    if "RAM" in product_i['specifications']:
        search_string += " " +  product_i['specifications']['RAM']
    if "storage" in product_i['specifications'] and product_i['type'] != 'mobile':
        search_string += " " +  product_i['specifications']['storage']
    if "battery" in product_i['specifications']:
        search_string += " " +  product_i['specifications']['battery']
    if "camera" in product_i['specifications']:
        search_string += " " +  product_i['specifications']['camera']

    return search_string
def get_competitor_products(product_i):
    search_string = get_search_string(product_i)
    
    try:
        productsFlipkart = get_flipkart_products(search_string)
        productsFlipkart, productsAmazon = get_amazon_price_by_fproducts_list(productsFlipkart, product_i['type'])

        overall = get_overall_products(productsAmazon, productsFlipkart, product_i['type'])

        return overall
    except Exception as e:
        print(e)
        raise e
