import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

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


def crawl_with_zenrows(url):
    all_products = []
    with tqdm(total=50) as pbar:
        for page_number in range(1, 51):
            params = {
                'url': f"{url}/p{page_number}",
                'apikey': 'fbda2bc1d8a35edf5bfdf3f2dad6b66de5c73e50',
                'premium_proxy': 'true',
            }
            response = requests.get(
                'https://api.zenrows.com/v1/', params=params)

            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, "html.parser")
                product_elements = soup.find_all("div", {"class": "js__card"})

                for product in product_elements:
                    all_products.append(extract_data_from_product(product))
            else:
                print(f"Failed to fetch data from page {page_number}")
                break

            pbar.update(1)

    return all_products


all_products = crawl_with_zenrows(base_url)

if all_products:
    df = pd.DataFrame(all_products)

    df.to_csv("products_data.csv", index=False)
    print("Data from 50 pages saved to 'products_data.csv'")
    df.to_json("products_data.json", orient="records")
    print("Data from 50 pages saved to 'products_data.json'")
else:
    print("No data to save.")
