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
        print('Choose an option :')
        print('1. Paste a Shopify link')
        print('2. Search a product with keywords')
        choice = input('Type the the number you want : ')
        while (choice != '11') and (choice != '22'):
            if choice == '1':
                URL = input('Paste a Shopify link ')
                if '?' in URL:
                    URL, y, z = URL.partition('?')
            elif choice == '2':
                website = input('On which site you want to cop ? Only type the domain name (eg: kith.com) ')
                keyword1 = input('Keyword 1 : ')
                keyword2 = input('Keyword 2 : ')
                keyword3 = input('Keyword 3 or leave a blank : ')
                keyword4 = input('Keyword 4 or leave a blank : ')
                keyword5 = input('Keyword 5 or leave a blank : ')
                keyword6 = input('Keyword 6 or leave a blank : ')
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
                                            print("(!)If the link is incorrect, then you made a mistake (!)")
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
        choice = input('Buy ? (y/n) ')
        while (choice != 'y1') and (choice != 'n1'):
            if choice == 'y':
                size = input('Size ? ')
                quantity = input('Quantity ? ')
                try:
                    variant = soup.find(text=size).findPrevious('id').text
                except AttributeError:
                    print('')
                    print("(!)Didnt found the size wanted, make sure to put the size as the list is saying (eg: If the list says Medium, then type medium, not just M) CAPS//SMALL IS IMPORTANT (!)")
                    print('')
                    print("Try Again...")
                    size = input('Size ?')
                    variant = soup.find(text=size).findPrevious('id').text
                url = urlparse(URL)
                baseurl = 'https://'+url.netloc+'/cart/'
                BD = baseurl+variant+':'+quantity
                driver = webdriver.Chrome()
                driver.get(BD)
                [getURL(), getSoup(), getItem(), getSize(), getStock(), getPrice(), getVariants(), getTotal(), formatData(), ATC()]
            elif choice == 'n':
                    choice1 = input('Do you want to seach another product ? (y/n) ')
                    while (choice1 != 'yo') and (choice1 != 'no'):
                        if choice1 == 'y':
                            [getURL(), getSoup(), getItem(), getSize(), getStock(), getPrice(), getVariants(), getTotal(), formatData(), ATC()]
                        else:
                            print('Ok, i close the shopify checker')
                            sys.exit()

    ATC()
