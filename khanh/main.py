import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
from tqdm import tqdm

base_url = "https://batdongsan.com.vn/nha-dat-ban"


def extract_data(product):
    def extract_element(parent, selector, attribute=None):
        element = parent.select_one(selector)
        return (
            element[attribute]
            if element and attribute in element.attrs
            else element.text.strip()
            if element
            else None
        )

    def extract_title(parent):
        return extract_element(parent, "span.pr-title.js__card-title", "aria-label")

    def extract_image_data(parent):
        image_data = parent.select_one("div.re__card-image img")
        return (
            image_data["data-img"]
            if image_data and "data-img" in image_data.attrs
            else None
        )

    data = {
        "prid": product.get("prid"),
        "title": extract_title(product),
        "location": extract_element(product, "div.re__card-location"),
        "time_published": extract_element(
            product, "span.re__card-published-info-published-at", "aria-label"
        ),
        "price": extract_element(product, "span.re__card-config-price"),
        "acreage": extract_element(product, "span.re__card-config-area"),
        "price_per_m2": extract_element(product, "span.re__card-config-price_per_m2"),
        "bedrooms": extract_element(product, "span.re__card-config-bedroom"),
        "bathrooms": extract_element(product, "span.re__card-config-toilet"),
        "product_url": base_url
        + extract_element(product, "a.js__product-link-for-product-id", "href"),
        "main_image": extract_image_data(product),
        "description": extract_element(
            product, "div.re__card-description.js__card-description"
        ),
    }

    return data


def crawl_with_zenrows(url, num_pages=50):
    all_products = []
    with tqdm(total=num_pages) as pbar:
        for page_number in range(1, num_pages + 1):
            params = {
                "url": f"{url}/p{page_number}",
                "apikey": "ae2f104a13b67d0c5e17114e630974f58927efd2",
                "premium_proxy": "true",
            }
            response = requests.get("https://api.zenrows.com/v1/", params=params)

            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, "html.parser")
                product_elements = soup.find_all("div", {"class": "js__card"})

                for product in product_elements:
                    all_products.append(extract_data(product))

                pbar.update(1)
            else:
                print(f"Failed to fetch data from page {page_number}")
                break

    return all_products


all_products = crawl_with_zenrows(base_url, num_pages=50)

if all_products:
    df = pd.DataFrame(all_products)

    csv_path = os.path.join("khanh", "data.csv")

    df.to_csv(csv_path, index=False)
    print(f"Data saved to '{csv_path}'")
else:
    print("No data to save.")
