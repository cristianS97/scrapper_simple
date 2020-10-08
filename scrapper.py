from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import os

ruta = os.path.dirname(os.path.abspath(__file__))

url = 'https://www.newegg.com/p/pl?d=graphics+card'

cliente = urlopen(url)

html = cliente.read()

cliente.close()

data = BeautifulSoup(html, 'html.parser')

# print(data.h1)
# print(data.p)
# print(data.body.span)

containers = data.find_all('div', {'class': 'item-container'})

data = {
    "brand": [],
    "product": [],
    "shipping": []
}

for container in containers:
    try:
        brand = container.div.div.a.img["title"]
        data['brand'].append(brand)
    except:
        data['brand'].append(None)

    try:
        title_container = container.findAll("a", {"class": "item-title"})
        product_name = title_container[0].text
        data['product'].append(product_name)
    except:
        data['product'].append(None)
        
    try:
        shipping_container = container.findAll("li", {"class": "price-ship"})
        shipping = shipping_container[0].text.strip()
        data['shipping'].append(shipping)
    except:
        data['shipping'].append(None)


pd.DataFrame(data).to_csv(os.path.join(ruta, 'data.csv'), sep=';', index=False)