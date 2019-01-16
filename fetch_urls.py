import requests
from bs4 import BeautifulSoup
import re
from googletrans import Translator
import json
import xlsxwriter, csv
import pandas as pd

translator = Translator()

def get_item_details(link):
    # Items to be fetched 
    # SKU, Product Name, Category and Sub Category, Page URL
    # Description Html, Specification HTML, Catalogue URL, IMage link
    # Attributes Separate from Specification into(Column): Size/Dimensions/Weight/Pieces and etc.*reference

    title_list = []
    item_page_req = requests.get(link).text
    item_page_soup = BeautifulSoup(item_page_req, 'html.parser')
    title = item_page_soup.find("div", attrs={"class": "text-description"})
    for name in title.text.replace(' ', '').split("\n"):
        if name != "":
            title_list.append(name)
    sku_code = translator.translate(title_list[0]).text.split(':')[1]
    product_name = translator.translate(title_list[1]).text.split(':')[1]
    product_url = link
    description = item_page_soup.find("div", attrs={"class": "details-panel-box extra-features"}).find("div",attrs={"class":"content-box"} )
    specification = item_page_soup.find("div", attrs={"class": "details-panel-box"}).find("div",attrs={"class":"content-box"} )
    desc_html = translator.translate(str(description)).text
    spec_html = translator.translate(str(specification)).text

    # Get the Speicfication Attributes
    attributes = {}
    attributes_html  = specification.find("ul", attrs={"class":"list-style-seven"}).find_all('li', attrs={"class": "clearfix"})
    for each in attributes_html:
        attributes[translator.translate(each.find("span", attrs={"class":"ttl"}).text).text] = translator.translate(each.find("span", attrs={"class":"dtl"}).text).text
    images_urls = []
    images_html = item_page_soup.find("ul", attrs={"class":"prod-image-carousel owl-theme owl-carousel"}).find_all("img")
    for image in images_html:
        images_urls.append(image)
    # data = {'sku':sku_code,
    #         'product_name':product_name,
    #         'product_url':product_url,
    #         'description_html':desc_html,
    #         'specification_html':spec_html,
    #         'images':images_urls}
    return list(attributes.keys())
    

# print(get_item_details('http://en.satatools.com/Product/show-62701.html'))

