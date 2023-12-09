from selectorlib import Extractor
from web_scrape.utilities import getHtml
import time
table_selector = '''
rows:
    css: 'table._14cfVK tr'
    xpath: null
    multiple: true
    type: HTML
price: 
    css: div._30jeq3._16Jk6d
    multiple: false
    type: Text
'''
row_selector = '''
key: 
    css: td._1hKmbr
    multiple: false
    type: Text
value: 
    css: td.URwL2w
    multiple: false
    type: Text
'''

extractor = Extractor.from_yaml_string(table_selector)
cellExtractor = Extractor.from_yaml_string(row_selector)
def get_laptop_details(raw):
    details = {}

    if "Processor Brand" in raw:
        details["processor"] = raw["Processor Brand"]

    if "Processor Name" in raw:
        if "processor" in details:
            details["processor"] += " " + raw['Processor Name']
        else:
            details["processor"] = raw['Processor Name']

    if "Processor Variant" in raw:
        if "processor" in details:
            details["processor"] += " " + raw['Processor Variant']
        else:
            details["processor"] = raw['Processor Variant']

    if "Graphic Processor" in raw:
        details["graphics"] = raw['Graphic Processor']

    if "RAM" in raw:
        details["RAM"] = raw['RAM']

    if "SSD Capacity" in raw:
        details['storage'] = raw['SSD Capacity']
    elif "HDD Capacity" in raw:
        details['storage'] = raw['HDD Capacity']

    if "Screen Size" in raw:
        details['display'] = raw['Screen Size']

    if "Screen Resolution" in raw:
        if "display" in details:
            details["display"] += raw['Screen Resolution']
        else:
            details["display"] = raw['Screen Resolution']

    if "Screen Type" in raw:
        details['display_type'] = raw['Screen Type']

    if "price" in raw:
        details['price'] = int(raw['price'].replace(",", '').replace("₹", ''))

    if "Model Name" in raw:
        details['model'] = raw['Model Name']

    if "Part Number" in raw:
        details['Part Number'] = raw['Part Number']

    return details

def get_mobile_details(raw):
    details = {}

    if "Battery Capacity" in raw:
        details['battery'] = raw['Battery Capacity']

    if "Processor Type" in raw:
        details["processor"] = raw["Processor Type"]

    if "Processor Core" in raw:
        if "processor" in details:
            details["processor"] += " " + raw['Processor Core']
        else:
            details["processor"] = raw['Processor Core']

    if "Primary Clock Speed" in raw:
        if "processor" in details:
            details["processor"] += " " + raw['Primary Clock Speed']
        else:
            details["processor"] = raw['Primary Clock Speed']

    if "Primary Camera" in raw:
        details["camera"] = raw['Primary Camera']

    if "RAM" in raw:
        details["RAM"] = raw['RAM']

    if "Internal Storage" in raw:
        details['storage'] = raw['Internal Storage']

    if "Display Size" in raw:
        details['display'] = raw['Display Size']

    if "Resolution" in raw:
        if "display" in details:
            details["display"] += raw['Resolution']
        else:
            details["display"] = raw['Resolution']

    if "Display Type" in raw:
        details['display_type'] = raw['Display Type']

    if "price" in raw:
        details['price'] = int(raw['price'].replace(",", '').replace("₹", ''))

    if "Model Name" in raw:
        details['model'] = raw['Model Name']

    return details

def get_specifications(url,type,html=None):
    if html == None:
        html = getHtml(url)
    data = extractor.extract(html)
    while data['rows'] == None:
        time.sleep(1)
        html = getHtml(url)
    specifications = {}
    for row in data['rows']:
        res = cellExtractor.extract(row)
        specifications[res['key'] ]= res['value']
    specifications['price'] = data['price']
    if type == 'laptop':
        return get_laptop_details(specifications)
    else:
        return get_mobile_details(specifications)
    

if __name__ == '__main__':
    url1 = "https://www.flipkart.com/samsung-galaxy-a23-blue-128-gb/p/itm493008f0e9f53?pid=MOBGCFVYJHGWNKSF&lid=LSTMOBGCFVYJHGWNKSFFI6SLL&marketplace=FLIPKART&q=Galaxy+A23+%288GB+RAM%29&store=tyy%2F4io&srno=s_1_7&otracker=search&otracker1=search&fm=Search&iid=3750d978-abe4-4e91-8a5b-58a55d6c0db1.MOBGCFVYJHGWNKSF.SEARCH&ppt=sp&ppn=sp&ssid=eddc8fkj0w0000001684163205609&qH=794ddeb83220d519"
    # url = "https://www.flipkart.com/hp-15s-intel-core-i5-12th-gen-8-gb-512-gb-ssd-windows-11-home-15s-fq5111tu-thin-light-laptop/p/itmbecf654716fd5?pid=COMGG63HGDTFCCGW&lid=LSTCOMGG63HGDTFCCGWLETTA9&marketplace=FLIPKART&q=HP+LAPTOP&store=6bo%2Fb5g&srno=s_1_1&otracker=search&otracker1=search&fm=Search&iid=39e01379-9f15-47d1-aeea-eea7e4a0511c.COMGG63HGDTFCCGW.SEARCH&ppt=pp&ppn=pp&ssid=wdq31j3gxc0000001684255890529&qH=ec946bfc1f9e0838"
    # url2 = 'https://www.flipkart.com/hp-pavilion-intel-core-i5-12th-gen-16-gb-512-gb-ssd-windows-11-home-2-graphics-15-eg2019tx-thin-light-laptop/p/itm74b5b6461da28?pid=COMGE2G5GVEZHPQP&lid=LSTCOMGE2G5GVEZHPQPEFMMCC&marketplace=FLIPKART&q=hp+pavilion+laptop+15+eg2019tx&store=search.flipkart.com&srno=s_1_1&otracker=search&otracker1=search&fm=search-autosuggest&iid=ea9ec84c-4b25-4f21-b714-dac720e6ec78.COMGE2G5GVEZHPQP.SEARCH&ppt=sp&ppn=sp&ssid=ooaihb7km80000001684392462479&qH=4149cbaf15983826'
    url2 = 'https://www.flipkart.com/hp-pavilion-eyesafe-2023-intel-core-i5-12th-gen-16-gb-512-gb-ssd-windows-11-home-eg2035tu-15-eg2035tu-thin-light-laptop/p/itm480cd128c58a0?pid=COMGDTTDKTZHWWJG&lid=LSTCOMGDTTDKTZHWWJGZ0D5GU&marketplace=FLIPKART&q=hP+15-Eg2035Tu&store=6bo&srno=s_1_1&otracker=search&otracker1=search&fm=Search&iid=10afdffa-3988-44c5-9157-2806934efa80.COMGDTTDKTZHWWJG.SEARCH&ppt=sp&ppn=sp&ssid=8fa9l1rups0000001684410067648&qH=023672f934dcaaad'
    d1 = get_specifications(url1, 'mobile')
    d2 = get_specifications(url2, 'laptop')

    print(d1,)
    print(d2)