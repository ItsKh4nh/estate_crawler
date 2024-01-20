import sqlite3
import json

conn = sqlite3.connect("demo_web/test.db")
cursor = conn.cursor()

with open("quan/bat_dong_san_vn.json", "r", encoding="utf-8") as file:
    data = json.load(file)

for item in data:
    title = item.get("title", "")
    price = item.get("price", "")
    acreage = item.get("acreage", "")
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
