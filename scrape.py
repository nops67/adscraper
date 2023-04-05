#1.1

import requests
from bs4 import BeautifulSoup
from random import randint
from time import sleep

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
        for match in soup.find_all('script'):
            if match.has_attr('src'):
                if 'googlesyndication' in match['src']:
                    try:
                        key = match['src'].split('-')[2]
                        break
                    except IndexError:
                        pass
                else:
                    key = "NO ADSENSE"
            else:
                key = "NO ADSENSE"
        print(url + " - " + key)
        with open(search + ".txt", 'a') as output:
            output.write(url + " - " + key + "\n")
        sleep(randint(2,5))
except requests.ConnectionError:
    pass
