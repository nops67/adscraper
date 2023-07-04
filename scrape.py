# 1.3

import requests
from bs4 import BeautifulSoup
from random import randint
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By                     
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

search = input("Search: ")

try:
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:111.0) Gecko/20100101 Firefox/111.0"}
    google_session = requests.Session()
    google_request = requests.get("https://www.google.pt/search?q=" + str(search) + "&num=50", headers=headers)
    google_soup = BeautifulSoup(google_request.content, 'lxml')

    for match in google_soup.find_all('div', class_="yuRUbf"):
        url = match.a['href']
        session = requests.Session()
        request = session.get(url, headers=headers)
        soup = BeautifulSoup(request.content, 'lxml')
        for script in soup.find_all('script'):
            if script.has_attr('src'):
                if 'googlesyndication' in script['src']:
                    try:
                        key = script['src'].split('-')[2]
                        break
                    except IndexError:
                        pass
                else:
                    key = "NO ADSENSE"
            else:
                key = "NO ADSENSE"
        print(url + " - " + key)
        with open(search + ".txt", 'a') as output:
            output.write(url + " - " + key)
        
            parsed_url = urlparse(url)
            opts = Options()
            opts.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:111.0) Gecko/20100101 Firefox/111.0")
            browser = webdriver.Firefox(options=opts)
            browser.get("https://www.similarweb.com/website/" + parsed_url.netloc)
            try:
                visits = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "engagement-list__item-value")))
                global_rank = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "wa-rank-list__value")))
            finally:
                output.write(" - Total Visits: " + visits.text + " ; Global Rank: " + global_rank.text + "\n")
                browser.implicitly_wait(randint(3, 5))
                browser.close()

except requests.ConnectionError:
    pass
