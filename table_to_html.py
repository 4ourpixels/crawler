import requests
from bs4 import BeautifulSoup

url = str("url")
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', class_='class')
    if links:
        categories = list(map(lambda link: link.text, links))
        hrefs = list(map(lambda link: link.get('href'), links))
        data_ids = list(map(lambda link: link.get('data-id'), links))

        # Create a minimal HTML table with Bootstrap styling
        html_table = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <title>Links Table</title>
        </head>
        <body>
            <div class="container mt-5">
                <table class="table">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">Category</th>
                            <th scope="col">Href</th>
                            <th scope="col">Data-id</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join(f"<tr><th scope='row'>{index + 1}</th><td>{category}</td><td>{href}</td><td>{data_id}</td></tr>" for index, (category, href, data_id) in enumerate(zip(categories, hrefs, data_ids)))}
                    </tbody>
                </table>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """

        # Save the HTML content to a file
        with open('results.html', 'w', encoding='utf-8') as file:
            file.write(html_table)
