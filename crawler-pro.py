import requests
from bs4 import BeautifulSoup

def fetch_links(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a', class_='class')
        hrefs = []

        if links:
            links_length = len(links)
            for index, link in enumerate(links, start=1):
                href_value = link.get('href')
                print(f"Saving {index} of {links_length}...")
                
                if href_value:
                    hrefs.append(href_value)
                    print(f'Saving Href: "{href_value}"')

            return hrefs

    return None

if __name__ == "__main__":
    url = "link"
    result = fetch_links(url)

    if result:
        print("Array of Hrefs:", result)
    else:
        print("Failed to fetch links.")
