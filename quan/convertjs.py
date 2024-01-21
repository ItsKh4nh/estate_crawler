import pandas as pd
import sqlite3
import os, json


def convert_price(price_str):
    if pd.isna(price_str) or "Thỏa thuận" in price_str:
        return 0
    elif "triệu" in price_str:
        return float(price_str.replace(" triệu", "")) * 1e6
    elif "tỷ" in price_str:
        return float(price_str.replace(" tỷ", "")) * 1e9
    else:
        return 0


def convert_acreage(acreage_str):
    if pd.isna(acreage_str):
        return 0
    else:
        return float(acreage_str.replace("m2", "").replace(",", "."))


conn = sqlite3.connect("demo_web/test.db")
cursor = conn.cursor()

with open("quan/bat_dong_san_vn.json", "r", encoding="utf-8") as file:
    data = json.load(file)

for item in data:
    title = item.get("title", "")
    price = convert_price(item.get("price", ""))
    acreage = convert_acreage(item.get("acreage", ""))
    description = item.get("description", "")
    main_image = item.get("image_url", "")
    source = "https://batdongsan.vn/"

    cursor.execute(
        "INSERT INTO products (title, price, acreage, description, main_image, source) VALUES (?, ?, ?, ?, ?, ?)",
        (title, price, acreage, description, main_image, source),
    )

conn.commit()
conn.close()

print(
    f"Data from 'quan/bat_dong_san_vn.json' has been imported into SQLite database 'demo_web/test.db'."
)
