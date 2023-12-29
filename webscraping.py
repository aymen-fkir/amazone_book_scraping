from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json

domain = "https://www.amazon.com"
url = f"{domain}/Books/s?srs=17143709011&rh=n%3A283155"

pages_data = dict()

def get_the_books_info(soup):
    try:
        target_book = "puisg-col puisg-col-4-of-12 puisg-col-8-of-16 puisg-col-12-of-20 puisg-col-12-of-24 puis-list-col-right"
        books = soup.find_all(class_=target_book)
        infos = dict()
        for book in books :
            name = book.find(class_="a-size-medium a-color-base a-text-normal")
            price_whole = book.find(class_ = "a-price-whole")
            price_fraction = book.find(class_ ="a-price-fraction")
            infos[name.text] = price_whole.text + price_fraction.text
    except:
        infos[None]=None
    return infos

def get_link(soup):
    try:

        target_class = "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"
        elements_with_class = soup.find_all(class_=target_class)
        link = elements_with_class[0].get("href")
    except:
        link=None
    return link

def get_page(url):

    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    req = Request(url, headers=header)
    page = urlopen(req)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    return soup
    

i = 0
while url!=None:           

    try:

        soup = get_page(url)
        infos = get_the_books_info(soup)
        key_name = f"page_{i}"
        i+=1
        pages_data[key_name] = [infos]
        print(i)
        url = f"{domain}{get_link(soup)}"
    except:
        with open("book_info.json", "w") as outfile: 
            json.dump(pages_data, outfile,indent=4)

    
with open("book_info.json", "w") as outfile: 
    json.dump(pages_data, outfile,indent=4)

