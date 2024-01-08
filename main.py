import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import cloudscraper
import time

base_url = "https://batdongsan.com.vn/nha-dat-ban"

def extract_data_from_product(product):
    def extract_element_text(parent, selector):
        element = parent.select_one(selector)
        return element.text.strip() if element else None

    def extract_image_src(parent, selector):
        element = parent.select_one(selector)
        return element["src"] if element else None

    data = {
        "prid": product.get("prid"),
        "title": product.select_one("a.js__product-link-for-product-id").get("title") if product.select_one("a.js__product-link-for-product-id") else None,
        "location": extract_element_text(product, "div.re__card-location"),
        "time_published": product.select_one("span.re__card-published-info-published-at").get("aria-label") if product.select_one("span.re__card-published-info-published-at") else None,
        "price": extract_element_text(product, "span.re__card-config-price"),
        "area": extract_element_text(product, "span.re__card-config-area"),
        "price_per_m2": extract_element_text(product, "span.re__card-config-price_per_m2"),
        "bedrooms": extract_element_text(product, "span.re__card-config-bedroom"),
        "bathrooms": extract_element_text(product, "span.re__card-config-toilet"),
        "agent_name": extract_element_text(product, "div.re__card-published-info-agent-profile-name"),
        "product_url": base_url + product.select_one("a.js__product-link-for-product-id").get("href") if product.select_one("a.js__product-link-for-product-id") else None,
        "agent_avatar": extract_image_src(product, "div.re__card-published-info-agent-profile-avatar img") if extract_image_src(product, "div.re__card-published-info-agent-profile-avatar img") else None,
        "main_image": product.select_one("div.re__img-child img[data-img]")["data-img"] if product.select_one("div.re__img-child img[data-img]") else None,
        "other_images": [img["data-src"] for img in product.select("div.re__img-child img[data-src]")],
        "description": extract_element_text(product, "div.re__card-description.js__card-description"),
    }

    return data


def crawl_all_pages(base_url):
    scraper = cloudscraper.create_scraper()
    all_products = []
    page_number = 1
    crawl_start_time = time.time()
    time_interval = 300
    
    with tqdm() as pbar:
        while True:
            url = f"{base_url}/p{page_number}"
            response = scraper.get(url)
            
            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, "html.parser")
                product_elements = soup.find_all("div", {"class": "js__card"})

                for product in product_elements:
                    all_products.append(extract_data_from_product(product))

                page_number += 1

                next_page_link = soup.find("link", {"rel": "next"})
                if not next_page_link:
                    break
                
                elapsed_time = time.time() - crawl_start_time
                if elapsed_time >= time_interval:
                    time.sleep(30)

            else:
                break
            pbar.update(1)

    return all_products

all_products = crawl_all_pages(base_url)

if all_products:
    df = pd.DataFrame(all_products)

    df.to_csv("products_data.csv", index=False)
    print("Dữ liệu từ trang đầu tiên đã được lưu vào file 'products-data.csv'")
    df.to_json("products_data.json", orient="records")
    print("Dữ liệu từ trang đầu tiên đã được lưu vào file 'products_data.json'")
else:
    print("Không có dữ liệu để lưu.")
