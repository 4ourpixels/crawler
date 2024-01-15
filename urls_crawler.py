import requests
from bs4 import BeautifulSoup
import json

class_name = "product-class"

def crawl_and_save(url, filename):
    response = requests.get(url)

    if response.status_code == 200:
        context = {}
        soup = BeautifulSoup(response.text, 'html.parser')
        product_elements = soup.find_all('li', class_=class_name)
        thumbnails = []
        hrefs = []

        for product_element in product_elements:
            a_tag = product_element.find('a')
            if a_tag:
                href = a_tag.get('href')
                hrefs.append(href)

                img_tag = product_element.find('img')
                if img_tag:
                    name = img_tag.get('alt') or img_tag.get('alt')
                    img_src = img_tag.get('data-src') or img_tag.get('src')
                    thumbnail = img_src
                    thumbnails.append(thumbnail)
                else:
                    print("No img tag found in the product.")
                print('-' * 40)

        products_info = []
        for href, thumbnail in zip(hrefs, thumbnails):
            product_info = {
                "href": href,
                "thumbnail": thumbnail,
                "name": name,
            }
            products_info.append(product_info)

        context.update({
            "products_info": products_info,
        })

        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(context, json_file, ensure_ascii=False, indent=4)

        print(f"Results for {url} saved to '{filename}'")
    else:
        print(f"Failed to fetch data from {url}")

# URLs to crawl
sofas = ""
chairs = ""
beds = ""

urls_and_filenames = [
    (sofas, 'sofas.json'),
    (chairs, 'chairs.json'),
    (beds, 'beds.json')
]

for url, filename in urls_and_filenames:
    crawl_and_save(url, filename)
