import pandas as pd
import sqlite3
import json


def convert_price(price_str):
    if pd.isna(price_str) or "Thỏa thuận" in price_str:
        return 0
    elif "triệu" in price_str:
        result = float(price_str.replace(" triệu", "")) * 1e6
    elif "tỷ" in price_str:
        result = float(price_str.replace(" tỷ", "")) * 1e9
    else:
        result = 0

    return 0 if result >= 1e11 else result


def convert_acreage(acreage_str):
    return (
        0
        if pd.isna(acreage_str)
        else float(acreage_str.replace("m2", "").replace(".", "").replace(",", "."))
    )


conn = sqlite3.connect("demo_web/test.db")
cursor = conn.cursor()

with open("quan/bat_dong_san_vn.json", "r", encoding="utf-8") as file:
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
        description, main_image, source = (
            item.get("description", ""),
            item.get("image_url", ""),
            "https://batdongsan.vn/",
        )

        cursor.execute(
            "INSERT INTO products (title, price, acreage, price_per_m2, description, main_image, source) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (title, price, acreage, price_per_m2, description, main_image, source),
        )

conn.commit()
conn.close()

print(
    f"Data from 'quan/bat_dong_san_vn.json' has been imported into SQLite database 'demo_web/test.db'."
)
