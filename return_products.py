import requests
from bs4 import BeautifulSoup

url = "link"
navbar_class = "class"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', class_=navbar_class)

    if links:
        categories = []
        hrefs = []
        data_ids = []

        for link in links:
            inner_url = link.get('href')
            inner_response = requests.get(inner_url)

            if inner_response.status_code == 200:
                inner_soup = BeautifulSoup(inner_response.text, 'html.parser')
                product_overview_items = inner_soup.find_all('li', class_='class')

                for idx, item in enumerate(product_overview_items):
                    if idx < 30:
                        print("Category:", link.text.strip())
                        print("Inner Link:", inner_url)
                        print("Product Overview Item Text:", item.text.strip())
                        print("-" * 50)
                        categories.append(link.text.strip())
                        hrefs.append(inner_url)
                        data_ids.append(item.text.strip())
