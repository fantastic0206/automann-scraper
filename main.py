import requests
import json
import os
import time
import random
from get_product_item_detail_url import scrape_product_item_detail_urls
from product_scraper import scrape_product_info
from bs4 import BeautifulSoup
from openpyxl import Workbook

# Define your login credentials
# username = ''
# password = ''

# Create a session to handle authentication and cookies
session = requests.Session()

# Send a POST request to the login page to authenticate
# login_url = 'https://www.automann.com/customer/account/loginPost/'
# login_data = {
#     'login[username]': username,
#     'login[password]': password,
#     'send': ''
# }
# login_response = session.post(login_url, data=login_data)

# Now that you're logged in, you can send a request to the URL you want to scrape
# url = 'https://www.automann.com/hvac/actuators/freightliner-stepper-motor-actuator-577-46555.html'
headers = {
    'cookie': '_ga=GA1.1.1297618546.1715261847; last_visited_store=default; login_redirect=https%3A%2F%2Fwww.automann.com%2F; PHPSESSID=4584f196d2ef4b21ddb63684aef6be6d; form_key=D46x6jibzfXU7YTG; X-Magento-Vary=98a11fad9d4ce4ef25efc4a4cc61d84271291912b0570f33b48f01e39b674b7d; mage-cache-sessid=true; _ga_ESYTQSFT2D=GS1.1.1715281153.3.1.1715281163.50.0.597775068; section_data_ids=%7B%22messages%22%3A1715281198%2C%22customer%22%3A1715281198%2C%22compare-products%22%3A1715281198%2C%22cart%22%3A1715281198%2C%22directory-data%22%3A1715281198%2C%22captcha%22%3A1715281198%2C%22instant-purchase%22%3A1715281198%2C%22persistent%22%3A1715281198%2C%22review%22%3A1715281198%2C%22wishlist%22%3A1715281198%2C%22mst-tm-addtocart%22%3A1715281198%2C%22multiwishlist%22%3A1715281198%2C%22hyva_checkout%22%3A1715281198%2C%22gtm%22%3A1715281198%2C%22recently_viewed_product%22%3A1715281198%2C%22recently_compared_product%22%3A1715281198%2C%22product_data_storage%22%3A1715281198%7D; private_content_version=8d9bc69cfb288269eef03c5e5bf97787'
}

# Initialize Excel workbook and sheet
wb = Workbook()
wb.active.title = "Scraped Data"

# Check if login was successful
# if login_response.status_code == 200:

# Get Navigation from Main URL
main_url = 'https://www.automann.com/'
response = session.get(main_url, headers=headers)

if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    category_lists = soup.find('div', class_='homepage-category-list').find_all('li')
    
    # File path to save JSON data
    file_path = 'product_item_detail_url.json'
    
    if os.path.isfile(file_path):
        if os.path.getsize(file_path) > 0:
            with open(file_path, 'r') as json_file:
                product_item_detail_url_ary = json.load(json_file)

            for index, product_item_detail_url in enumerate(product_item_detail_url_ary):
                scrape_product_info(product_item_detail_url, session, headers, wb, index)

                #if index % 1000 == 0:
                random_time = random.randint(1, 3) / 10
                time.sleep(random_time)
    else:
        product_item_detail_url_ary = []
            
        for index, category_list in enumerate(category_lists):
            category_url = category_list.find('a')['href']
            product_item_detail_urls = scrape_product_item_detail_urls(category_url, session, headers, index)
            if product_item_detail_urls is not None:
                product_item_detail_url_ary.extend(product_item_detail_urls)

        print(f"product item detail page total count: {len(product_item_detail_url_ary)}")

        # Writing array to JSON file
        with open(file_path, 'w') as json_file:
            json.dump(product_item_detail_url_ary, json_file)

        print('Your product item detail url json file exported successfully!')

    # # Save Excel file
    wb.save('product_info.xlsx')
    print('Your excel file exported successfully!')

# else:
#     print('Login failed')
