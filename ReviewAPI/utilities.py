import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")

chrome_options.add_argument("--log-level=3")
browser = webdriver.Chrome(options=chrome_options)
# browser.set_page_load_timeout(10)

headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

def getHtml(url, mode="selenium", read_more_element_class=None):
    if mode == "selenium":
        browser.get(url)
        if read_more_element_class:
            rm_btns = browser.find_elements(By.CLASS_NAME , read_more_element_class)
            for rm_btn in rm_btns:
                rm_btn.click()
        return browser.page_source
    
    else:
        r = requests.get(url, headers=headers)
        return r.text
