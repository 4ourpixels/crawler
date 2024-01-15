import requests
from bs4 import BeautifulSoup
import json

sofas = ""
chairs = ""
beds = ""

urls = set(sofas, chairs, beds)

url = ""

navbar_class = "product-class"

response = requests.get(url)

if response.status_code == 200:
    context = {}
    soup = BeautifulSoup(response.text, 'html.parser')
    product_elements = soup.find_all('li', class_='product-class')
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

    # Save the results to a JSON file
    with open('results.json', 'w', encoding='utf-8') as json_file:
        json.dump(context, json_file, ensure_ascii=False, indent=4)

    print("Results saved to 'results.json'")
