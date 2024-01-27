import pandas as pd
import sqlite3, json
from datetime import datetime


def convert_price(price_str):
    if pd.isna(price_str):
        return 0
    else:
        return float(price_str)


def convert_area(area_str):
    if pd.isna(area_str):
        return 0
    if "-" in area_str:
        start, end = map(
            float,
            area_str.replace("m2", "").replace(".", "").replace(",", "").split("-"),
        )
        return (start + end) / 2
    else:
        return float(area_str.replace("m2", "").replace(".", "").replace(",", ""))


def extract_location(address):
    parts = address.split(", ")
    district_part = parts[-2].replace("Quận", "").replace("Huyện", "").strip()
    if any(char.isdigit() for char in district_part):
        district = parts[-2].strip()
    else:
        district = district_part

    city = (
        parts[-1].replace("Tỉnh", "").replace("Thành phố", "").replace("TP", "").strip()
    )
    return district, city


conn = sqlite3.connect("demo_web/data.db")
cursor = conn.cursor()

with open("VietAnh/Bds1.json", "r", encoding="utf-8") as file:
    data = json.load(file)

for item in data:
    id, title, price, area = (
        item.get("id", ""),
        item.get("title", ""),
        convert_price(item.get("price", "")),
        convert_area(item.get("area", "")),
    )

    if area > 10:
        time_str = item.get("time", "")
        time = datetime.strptime(time_str, "%d/%m/%Y") if time_str else None

        address = item.get("address", "")
        district, city = extract_location(address)

        price_per_m2 = round(price / area) if price and area and area != 0 else 0
        description, url, image, source = (
            item.get("description", ""),
            item.get("url", ""),
            item.get("image", ""),
            "https://homedy.com/",
        )

        cursor.execute(
            "INSERT INTO products (prid, title, time_published, district, city, price, acreage, price_per_m2, description, product_url, main_image, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                id,
                title,
                time.date() if time else None,
                district,
                city,
                price,
                area,
                price_per_m2,
                description,
                url,
                image,
                source,
            ),
        )

conn.commit()
conn.close()

print(
    f"Data from 'VietAnh/Bds1.json' has been imported into SQLite database 'demo_web/data.db'."
)
