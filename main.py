import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from pprint import pprint
import pandas as pd 
import re, os
from requests_testadapter import Resp
from fetch_urls import get_item_details

class LocalFileAdapter(requests.adapters.HTTPAdapter):
    def build_response_from_file(self, request):
        file_path = request.url[7:]
        with open(file_path, 'rb') as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            r = self.build_response(request, resp)

            return r

    def send(self, request, stream=False, timeout=None,
             verify=True, cert=None, proxies=None):

        return self.build_response_from_file(request)

requests_session = requests.session()
requests_session.mount('file://', LocalFileAdapter())

url = 'file://translated.html'
html_page = requests_session.get(url).text
soup = BeautifulSoup(html_page, 'html.parser')

x = []
for link in soup.findAll('a'):#, attrs={'href': re.compile("^http://en.satatools.com")}):
    if link.text:
        # print ("{}: http://en.satatools.com{}".format(link.text,link.get('href')))
        full_link = "http://en.satatools.com{}".format(link.get('href'))
        x.append([link.text,full_link])
# print(x[:x.index('Power tool')])
y = ['Electrical Electronics Tools', 'Electronic Soldering Tools', 'Detecting Instrumentation', 'Hot Air Gun Series', 'Lighting Appliances', 'Electrical and Electronics Suite', 'Electronic pliers', 'Cable Tools', 'Electrical Repair Tools', 'Micro Screwdriver', 'Other electronic tools', '动力工具', 'Power Tools', 'Pneumatic Tools', 'Wind Sleeve', ' Lifting Hydraulic pressure', ' Lifting Tools', 'Hydraulic Tools', 'Integrated Team Set', 'Tool Storage', 'Sleeve and Accessories', ' Handsets ',
'Torque Wrench', ' Inner hexagon ', 'Screwdriver head', 'Pliers Tools', 'Cutting Tools', 'Tapping Tools', 'Measuring Tools', 'Pipeline Tools', 'VDE Insulation Tools', 'Abrasive Abrasives', 'Other hand tools', '汽保设备', 'Car Diagnostics', 'Raising devices', 'Tire Equipment', 'Tire Inflator', 'Air compressor', 'Oil Equipment', 'Hydraulic Equipment', '卧顶', 'Battery and Circuitry', ' Auto Repair Auto Maintenance Tools', 'Tire Repair Tools', 'Roller reel', 'Auto Repair Tool Set', 'Lubricating Equipment & Tools', 'Tire Inflator', 'Engine Repair Tools', 'Chassis Repair Tools', 'Car Body Repair Tools', 'Electrical Repair Tools', '网络专供', 'Building Tools', 'Home Series', ' Personal Protection Supplies', 'Head protection', 'Eye Protection', 'Listening protection', 'Respiratory Protection', 'Body protection', 'Hand Protection', 'foot protection']

# Get sub category links of the individual items
def get_item_lists(link):# Takes Sub Category link
    page_req = requests.get(link).text
    page_soup = BeautifulSoup(page_req, 'html.parser')
    # sub_category_links = []
    try:
        items = page_soup.find_all("div", attrs={"class":"title-box"})
        for each in items:
            items_links = each.find("a")
            # ITem links per page or sub category
            return 'http://en.satatools.com{}'.format(items_links.get('href'))
        # return **sub_category_links #retyrns a list of url of all items on that page
    except:
        print ("caught it")

attrs_set = set()
for each in x:
    # head = get_item_lists(each[1])
    attrs_set.add(x for x in get_item_details(get_item_lists(each[1])))
    # print (head)

print(attrs_set)

