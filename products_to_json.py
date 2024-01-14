import requests
from bs4 import BeautifulSoup
import json

url = "link"
navbar_class = "class"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', class_=navbar_class)

    results = []  # List to store the results

    if links:
        for link in links:
            inner_url = link.get('href')
            inner_response = requests.get(inner_url)

            if inner_response.status_code == 200:
                inner_soup = BeautifulSoup(inner_response.text, 'html.parser')
                product_overview_items = inner_soup.find_all('li', class_='class')

                for idx, item in enumerate(product_overview_items):
                    # Dictionary to store the result for each item
                    result_dict = {
                        "category": link.text.strip(),
                        "inner_link": inner_url,
                        "data": []
                    }

                    # Extract information from <a> tags with specified data attributes
                    a_tags = item.find_all('a', {'data-item-id': True, 'data-item-type': True, 'data-navi-area-id': True})
                    for a_tag in a_tags:
                        href = a_tag.get('href')
                        data_item_id = a_tag.get('data-item-id')
                        data_item_type = a_tag.get('data-item-type')
                        data_navi_area_id = a_tag.get('data-navi-area-id')
                        title = a_tag.get('title', "")

                        # Append data to the result_dict
                        result_dict["data"].append({
                            "href": href,
                            "data-item-id": data_item_id,
                            "data-item-type": data_item_type,
                            "data-navi-area-id": data_navi_area_id,
                            "title": title
                        })

                    # Extract image src urls of lazyloaded images
                    lazyloaded_images = item.select('img.lazyloaded')
                    for img in lazyloaded_images:
                        img_src = img.get('data-src')
                        result_dict["data"].append({"image_src": img_src})

                    # Append the result_dict to the results list
                    results.append(result_dict)

    # Save the results list to a JSON file
    with open('products.json', 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, indent=2)
