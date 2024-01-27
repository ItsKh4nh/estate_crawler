import pandas as pd
import sqlite3
import json


def convert_price(price_str):
    if pd.isna(price_str) or "Giá thỏa thuận" in price_str or "m2" in price_str:
        return 0
    elif "triệu" in price_str:
        return int(
            float(price_str.replace(" triệu", "").replace(".", "").replace(",", "."))
            * 1e6
        )
    elif "tỷ" in price_str:
        return int(
            float(price_str.replace(" tỷ", "").replace(".", "").replace(",", ".")) * 1e9
        )
    else:
        return 0


def convert_acreage(acreage_str):
    if pd.isna(acreage_str):
        return 0
    if "-" in acreage_str:
        start, end = map(
            float,
            acreage_str.replace("m2", "").replace(".", "").replace(",", "").split("-"),
        )
        return (start + end) / 2
    else:
        return float(acreage_str.replace("m2", "").replace(".", "").replace(",", ""))


conn = sqlite3.connect("demo_web/data.db")
cursor = conn.cursor()

with open("LaDat/alonhadat.json", "r", encoding="utf-8") as file:
    data = json.load(file)

for item in data:
    title, price, acreage = (
        item.get("title", ""),
        convert_price(item.get("price", "")),
        convert_acreage(item.get("acreage", "")),
    )

    if acreage > 10:
        price_per_m2 = (
            round(price / acreage) if price and acreage and acreage != 0 else 0
        )
        description, main_image, product_url, source = (
            item.get("description", ""),
            item.get("image_url", ""),
            item.get("link", ""),
            "https://alonhadat.com.vn/",
        )

        cursor.execute(
            "INSERT INTO products (title, price, acreage, price_per_m2, description, main_image, product_url, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                title,
                price,
                acreage,
                price_per_m2,
                description,
                main_image,
                product_url,
                source,
            ),
        )

conn.commit()
conn.close()

print(
    f"Data from 'LaDat/alonhadat.json' has been imported into SQLite database 'demo_web/data.db'."
)
