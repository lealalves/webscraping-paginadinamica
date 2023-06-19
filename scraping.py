import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math

url = 'https://www.kabum.com.br/espaco-gamer/cadeiras-gamer'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')

qtd_itens = soup.find('div', id='listingCount').get_text().split(' ')[0]

qtd_pagina = math.ceil(int(qtd_itens)/20)

dict_produtos = {'marca': [], 'preco': []}

for i in range(1, qtd_pagina+1):
    url_page = f'https://www.kabum.com.br/espaco-gamer/cadeiras-gamer?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    site = requests.get(url_page, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    produtos = soup.findAll('div', class_=re.compile('productCard'))

    for produto in produtos:
        marca = produto.find('span', class_=re.compile('nameCard')).get_text(strip=True)
        preco = produto.find('span', class_=re.compile('priceCard')).get_text(strip=True)

        dict_produtos['marca'].append(marca)
        dict_produtos['preco'].append(preco)
        print(marca, preco)
    print(url_page)

df = pd.DataFrame(dict_produtos)
df.to_csv('preco_cadeiras.csv', encoding='utf-8', sep=';')