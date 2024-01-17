"""
//Web Scraping for Product Information

This Python script is designed for web scraping product 
information from a series of URLs specified in the urls list. 
The target websites contain product listings, and the script 
utilizes the requests library for making HTTP requests, 
BeautifulSoup for HTML parsing, and json for data serialization.

Key Functions:

// Scraping Product Images:

The get_product_images function extracts product images with the 
file extensions .jpg or .jpeg from the provided URL.

// Scraping Product Descriptions:

The get_product_description function extracts product descriptions 
from the provided URL.

// Scraping Product Image Information:

The get_product_img function attempts to retrieve additional 
information about product images, including source and alt text.

// Extracting Product Details:

Functions like get_product_name, get_product_category, and 
get_product_brand extract specific details from the product's alt text.

// Main Scraping Loop:

The program iterates through each URL in the urls list.
For each URL, it extracts product information such as name, 
category, brand, description, and images.

// Saving Results:

The collected product information is stored in a list called 
all_products_info.
The final data is serialized into a JSON file named data.json 
using the json.dump function.

// Usage:

Specify the URLs to scrape by populating the urls list.
Run the script.
The script will iterate through each URL, scrape product 
information, and save the results in a structured JSON format.

// Dependencies:

requests: For making HTTP requests.
BeautifulSoup: For HTML parsing.
json: For handling JSON data.
tqdm: For displaying progress bars during the scraping process.

"""

import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

# List of URLs to scrape
urls = [
    # Add URLs
]

# Important to initialize an empty list to store results for all URLs
all_products_info = []

def calculate_percentage(part, whole):
    try:
        percentage = (part / whole) * 100
        return percentage
    except ZeroDivisionError:
        return "Cannot divide by zero."

# Function to get product images with .jpg or .jpeg extensions
def get_product_images(href):
    product_class = "lazyload"
    valid_extensions = {".jpeg", ".jpg"}
    try:
        response = requests.get(href)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_image_elements = soup.find_all('img', class_=product_class)
            product_images = []
            for element in product_image_elements:
                img_src = element.get('data-src') or element.get('src')
                if any(img_src.lower().endswith(ext) for ext in valid_extensions):
                    product_images.append(img_src)
            return product_images
        else:
            print(f"Failed to retrieve content from {href}. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error occurred while crawling {href}: {str(e)}")
        return []

# Function to get product description
def get_product_description(href):
    product_class = "description-text"
    try:
        response = requests.get(href)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_description_elements = soup.find_all('span', class_=product_class)
            if product_description_elements:
                description = [element.get_text(strip=True) for element in product_description_elements]
                return description[0]
            else:
                return "No Description"
        else:
            print(f"Failed to retrieve content from {href}. Status code: {response.status_code}")
            return "No Description"
    except Exception as e:
        print(f"Error occurred while crawling {href}: {str(e)}")
        return "No Description"

# Function to get product images with additional information
def get_product_img(href):
    try:
        response = requests.get(href)
        image_dictionary = {}
        results = {}
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img', {'data-src': True, 'alt': True, 'class': 'lazyload'})
            for image in img_tags:
                src = image.get('data-src')
                alt = image.get('alt')
                image_dictionary.append({
                    "src": src,
                    "alt": alt,
                })
            lazyloaded_images = image.select('img.lazyloaded')
            for img in lazyloaded_images:
                img_src = img.get('data-src')
                image_dictionary["data"].append({"image_src": img_src})

            results.update({image_dictionary})
        return results
    except Exception as e:
        print(f"Error occurred while crawling {href}: {str(e)}")
        return "No Description"

# Function to extract product name from alt attribute
def get_product_name(alt):
    return alt.split('|')[0].strip()

# Function to extract product category from alt attribute
def get_product_category(alt):
    return alt.split('|')[1].strip()

# Function to extract product brand from alt attribute
def get_product_brand(alt):
    return alt.split('|')[2].strip()

# Iterate through each URL
for url in urls:
    response = requests.get(url)
    
    if response.status_code == 200:
        context = {}
        soup = BeautifulSoup(response.text, 'html.parser')
        product_elements = soup.find_all('li', class_='product-overview')
        thumbnails = []
        hrefs = []
        product_images = []
        products_info = []
        product_id_counter = 1

        # Iterate through each product element
        for product_element in tqdm(product_elements, desc="Scraping Progress", unit="product"):
            a_tag = product_element.find('a')
            if a_tag:
                href = a_tag.get('href')
                hrefs.append(href)
                description = get_product_description(href)
                product_images = get_product_images(href)
                
                img_tag = product_element.find('img')
                
                if img_tag:
                    alt = img_tag.get('alt') or img_tag.get('alt')
                    name = get_product_name(alt)
                    category = get_product_category(alt)
                    brand = get_product_brand(alt)
                    img_src = img_tag.get('data-src') or img_tag.get('src')
                    thumbnail = img_src
                    product_images.append(thumbnail)
                else:
                    print("No img tag found in the product.")
                    
                percentage = calculate_percentage(product_id_counter, len(product_elements))
                print(f"{percentage:.2f}%")

                product_info = {
                    "id": product_id_counter,
                    "href": href,
                    "thumbnail": thumbnail,
                    "name": name,
                    "product_images": product_images,
                    "description": description,
                    "brand": brand,
                    "category": category,
                }
                products_info.append(product_info)
                product_id_counter += 1
        context.update({
            "products_info": products_info,
        })
        all_products_info.extend(products_info)

# Write all data to a single JSON file
with open('data.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_products_info, json_file, ensure_ascii=False, indent=4)

print("Results saved to 'data.json'")
