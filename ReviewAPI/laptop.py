import re

reg = {
    'dell' : '[A-Za-z0-9]{12,13}| [A-Za-z]+ [0-9]{4} ',
    'hp': '[0-9]{2}[a-zA-Z]{0,1}[ ]{0,1}-[ ]{0,1}[a-zA-Z0-9]+',
    'asus': '[a-zA-Z0-9]{6,9}[ ]{0,1}-[ ]{0,1}[a-zA-Z0-9]{6,8}',
    'lenovo': '[0-9]{2}[a-zA-Z][a-zA-Z0-9]{2,10}',
    'apple': '[a-zA-Z0-9]+/[a-zA-Z]$',
    'acer' : '[a-zA-Z0-9]+-[a-zA-Z0-9]{2,4}',
    'msi': '[a-zA-Z0-9]{3,4}-[a-zA-Z0-9]{5,6}',
    'redmibook': '*'
}


def getModelNumber(productName):
    try:
        brand = productName.split()[0].lower()
        model = re.findall(reg[ brand ],productName)[0]

        return brand +" " + model
    
    except:
        return productName
