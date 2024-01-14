import requests
from bs4 import BeautifulSoup
url = str("")
response = requests.get(url)
navbarClass = str("")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', class_=navbarClass)
    if links:
        categories = list(map(lambda link: link.text, links))
        hrefs = list(map(lambda link: link.get('href'), links))
        data_ids = list(map(lambda link: link.get('data-id'), links))