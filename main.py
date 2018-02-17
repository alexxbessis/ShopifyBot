from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlparse
import requests
import sys
import time
import lxml

print('Made by @alexxbessis')
while True:
    def getTime():
        return time.strftime('|%D | %H:%M:%S|')
    def getURL():
        print('___________________________________________________________________________________________________________________________________________________________')
        print('')
        global r
        global soup
        global URL
        print(getTime())
        print('')
        print('Choisis une option:')
        print('1. Coller un link Shopify')
        print('2. Rechercher un produit avec keywords')
        choice = input('Tape le numero que tu veux : ')
        while (choice != '11') and (choice != '22'):
            if choice == '1':
                URL = input('Colle un lien Shopify : ')
                if '?' in URL:
                    URL, y, z = URL.partition('?')
            elif choice == '2':
                website = input('Sur quel site tu veux cop ? Seulement taper nom de domaine (ex: kith.com) ')
                keyword1 = input('Keyword 1 : ')
                keyword2 = input('Keyword 2 : ')
                keyword3 = input('Keyword 3 ou laisse un vide : ')
                keyword4 = input('Keyword 4 ou laisse un vide : ')
                keyword5 = input('Keyword 5 ou laisse un vide : ')
                keyword6 = input('Keyword 6 ou laisse un vide : ')
                s = requests.Session()
                f = s.get('https://'+website+'/sitemap_products_1.xml')
                soup1 = BeautifulSoup(f.text, 'lxml')
                products = soup1.find_all('url')
                for url in products:
                    if keyword1 in url.get_text():
                        URL = (url.find('loc').text)
                        if keyword2.lower() in URL:
                            if keyword3.lower() in URL:
                                if keyword4.lower() in URL:
                                    if keyword5.lower() in URL:
                                        if keyword6.lower() in URL:
                                            print('')
                                            print('Product url: {}'.format(URL))
                                            print("(!)Si le lien est incorrect j'ai fais une connerie(!)")
                                            return URL

            break
    def getSoup():
        global soup
        s = requests.Session()
        r = s.get(URL+'.xml')
        soup = BeautifulSoup(r.text, 'lxml')
        return soup
    def getItem():
        global item
        item = soup.find('title').text
    def getSize():
        global sz
        sz = list()
        for size in soup.find_all('title')[1:]:
            sz.append(size.get_text())
        return sz
    def getStock():
        global stk
        stk = list()
        for stock in soup.find_all('inventory-quantity'):
            stk.append(stock.get_text())
        return stk
    def getPrice():
        global prc
        prc = list()
        for price in soup.find_all('price'):
            prc.append(price.get_text())
        return prc
    def getVariants():
        global vrnt
        vrnt = list()
        for variants in soup.find_all('product-id'):
            vrnt.append(variants.find_previous('id').get_text())
        return vrnt
    def getTotal():
        global ttl
        ttl = list()
        for stocktotal in soup.findAll("inventory-quantity"):
            ttl.append(int(stocktotal.text))
        return ttl
    [getURL(), getSoup(), getItem(), getSize(), getStock(), getPrice(), getVariants(), getTotal()]
    def formatData():
        print('')
        print(item)
        if len(stk)>0:
            print('{:<5} | {:<20} | {:<10} | {:10} | {:20} '.format('', 'size', 'stock', 'price', 'variants'))
            for i, (size, stock, price, variant) in enumerate(zip(sz, stk, prc, vrnt)):
                print('{:<5} | {:<20} | {:<10} | {:10} | {:20} '.format(i, size, stock, '$'+price, variant))
            if sum(ttl) == 0:
                print('Sold out!')
            elif sum(ttl) != 0:
                print('Total stock: {:<5}'.format(sum(ttl)))
        else:
            print('Jconnais ap le stock :(')
            print('{:<5} | {:<20} | {:10} | {:20} '.format('', 'size', 'price', 'variants'))
            for i, (size, price, variant) in enumerate(zip(sz, prc, vrnt)):
                print('{:<5} | {:<20} | {:10} | {:20} '.format(i, size, '$'+price, variant))
    formatData()
    def ATC():
        print('')
        choice = input('Acheter ? (y/n) ')
        while (choice != 'y1') and (choice != 'n1'):
            if choice == 'y':
                size = input('Quelle taille ? ')
                quantity = input('Quelle quantité ? ')
                try:
                    variant = soup.find(text=size).findPrevious('id').text
                except AttributeError:
                    print('')
                    print("(!)J'ai pas trouvé la taille, sois sur de mettre la taille sur le format comme la liste ci-dessus (ex: Si la liste dit Medium, ecris medium, pas juste M) MAJUSCULE//MINUSULE IMPORTE (!)")
                    print('')
                    print("Try Again...")
                    size = input('Quelle taille ?')
                    variant = soup.find(text=size).findPrevious('id').text
                url = urlparse(URL)
                baseurl = 'https://'+url.netloc+'/cart/'
                BD = baseurl+variant+':'+quantity
                driver = webdriver.Chrome()
                driver.get(BD)
                [getURL(), getSoup(), getItem(), getSize(), getStock(), getPrice(), getVariants(), getTotal(), formatData(), ATC()]
            elif choice == 'n':
                    choice1 = input('Tu veux chercher un autre produit ? (y/n) ')
                    while (choice1 != 'yo') and (choice1 != 'no'):
                        if choice1 == 'y':
                            [getURL(), getSoup(), getItem(), getSize(), getStock(), getPrice(), getVariants(), getTotal(), formatData(), ATC()]
                        else:
                            print('Ok, je ferme le shopify checker')
                            sys.exit()

    ATC()
