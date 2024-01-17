"""
The following code will extract and print the information/details of the product
on the terminal from the json_data.json file that contains the hrefs

// Features:

1. Gets page title
2. Gets the product title
3. Gets the product description
4. Returns a list of the source product images ending with .jpg & .png

"""
# Imports
import requests  # For making HTTP requests
import json  # For handling JSON data
from bs4 import BeautifulSoup  # For parsing HTML content

# Function to extract page title from BeautifulSoup object
def get_page_title(soup):
    raw_page_title = soup.title.string
    return raw_page_title.split('|')[0].strip()

# Function to extract product title from BeautifulSoup object
def get_product_title(soup):
    title_section = soup.find('section', class_='product-title')
    raw_product_title = title_section.find('h1', class_='text-5xl')
    return raw_product_title.string

# Function to extract product description from BeautifulSoup object
def get_product_description(soup, product_class="description-text"):
    product_description_elements = soup.find_all('span', class_=product_class)
    return [element.get_text(strip=True) for element in product_description_elements]

# Function to extract list items with images from BeautifulSoup object
def get_list_items_with_images(soup, list_class='product-overview'):
    product_gallery_section = soup.find('section', class_='product-gallery')
    if product_gallery_section:
        gallery_list_items = product_gallery_section.find_all('li', class_=list_class)
        return gallery_list_items
    else:
        return []

# Function to extract image URLs from list item
def extract_image_urls_from_list_item(li):
    list_item_images = li.find_all('img')
    return [img['src'] for img in list_item_images]

# Function to filter image URLs based on allowed extensions
def filter_image_urls(image_urls, allowed_extensions=('.jpg', '.png')):
    return [url for url in image_urls if url.lower().endswith(allowed_extensions)]

# Main function to crawl a given URL and print product information
def crawl_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extracting and printing page title
            page_title = get_page_title(soup)
            
            # Extracting and printing product title
            product_title = get_product_title(soup)
            print(f"PRODUCT NAME====>: {product_title}")

            # Extracting and printing product description
            product_description = get_product_description(soup)
            print(f"PRODUCT DESCRIPTION====>: {product_description[0] if product_description else 'No description found.'}\n")

            # Extracting and printing image URLs from list items
            gallery_list_items = get_list_items_with_images(soup)
            if gallery_list_items:
                for i, li in enumerate(gallery_list_items, 1):
                    image_urls = extract_image_urls_from_list_item(li)
                    filtered_image_urls = filter_image_urls(image_urls)
                    if filtered_image_urls:
                        print(f"PRODUCT IMAGE LINK {i}.)====>:{', '.join(filtered_image_urls)}")
                    else:
                        print(f"{i}. List Item with Images - No images with allowed extensions found.")
                print()
            else:
                print(f"No list items with images found in the product-gallery section on {url}")
        else:
            print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
    
    except Exception as e:
        print(f"Error occurred while crawling {url}: {str(e)}")

# Load JSON data from file
with open('json_data.json', 'r') as file:
    data = json.load(file)

# Print information for the first URL only
if data['data']:
    # Using zero-based indexing for Python
    first_url = data['data'][0]['href']
    crawl_url(first_url)
else:
    print("No URLs found in the JSON data.")
