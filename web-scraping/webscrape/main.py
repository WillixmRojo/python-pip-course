import requests
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Firefox(executable_path='py-project/web-scraping/geckdriver.exe')

driver.get('https://www.coppel.com')

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

categories_html = soup.find_all('li',{'class': 'menu-item'})

categories = []

for category in categories_html:
    name = category.find('a').text
    categories.append(name)

print(categories)
