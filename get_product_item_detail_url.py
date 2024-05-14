import requests
import math
from bs4 import BeautifulSoup
import time

def scrape_product_item_detail_urls(category_url, session, headers, index):
    url = 'https://www.automann.com' + category_url
    print(f"category url => {index + 1} => {url}")

    response = session.get(url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        toolbar_amount = soup.find('p', class_='toolbar-amount')
        if toolbar_amount:
            total_items = int(toolbar_amount.find_all('span')[2].text.strip())
            pageCount = math.ceil(total_items / 300)

            product_item_detail_urls = []

            for i in range(pageCount):
                pageurl = f"{url}?p={i + 1}&product_list_limit=300"
                print(f"page url => {i + 1} => {pageurl}")
                # time.sleep(5)
                page_response = session.get(pageurl, headers=headers)
                print(page_response.status_code)
                
                if page_response.status_code == 200:
                    page_soup = BeautifulSoup(page_response.content, 'html.parser')
                    product_items_container = page_soup.find('div', class_='category-products')
                    if product_items_container:
                        product_items1 = product_items_container.find('div', class_='products').find_all('form', class_='product-item')
                        product_items2 = product_items_container.find('div', class_='products').find_all('div', class_='product-item')

                        product_items = product_items1 + product_items2

                        for idx, product_item in enumerate(product_items):
                            product_item_url = product_item.find('div', class_='grid-item-container').find('div', class_='grid-item-top').find('a')['href']
                            print(f"prduct item url => {idx} => {product_item_url}")
                                
                            product_item_detail_urls.append(product_item_url)

            return product_item_detail_urls
        else:
            print("Toolbar amount not found on the page.")
    else:
        print(f"Failed to fetch page {url}. Status code: {response.status_code}")

