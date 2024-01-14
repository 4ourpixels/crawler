import requests
from bs4 import BeautifulSoup
import json
url = str("https://www.architonic.com/en")
response = requests.get(url)
navbarClass = str("mobile-menu-item")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', class_=navbarClass)
    if links:
        categories = list(map(lambda link: link.text, links))
        hrefs = list(map(lambda link: link.get('href'), links))
        data_ids = list(map(lambda link: link.get('data-id'), links))
        navlinks = [{"category": category, "href": href, "data-id": data_id} for category, href, data_id in zip(categories, hrefs, data_ids)]
        with open('navlinks.json', 'w', encoding='utf-8') as json_file:
            json.dump(navlinks, json_file, indent=2)