import pandas as pd
import sqlite3
import os


def convert_price(price_str):
    if pd.isna(price_str) or "Giá thỏa thuận" in price_str:
        return 0
    elif "triệu" in price_str:
        return int(
            float(price_str.replace(" triệu", "").replace(".", "").replace(",", "."))
            * 1000000
        )
    elif "tỷ" in price_str:
        return int(
            float(price_str.replace(" tỷ", "").replace(".", "").replace(",", "."))
            * 1000000000
        )
    else:
        return 0


def convert_acreage(acreage_str):
    if pd.isna(acreage_str):
        return 0
    else:
        return float(acreage_str.replace(" m²", "").replace(".", "").replace(",", "."))


csv_file = os.path.join("khanh", "data.csv")
df = pd.read_csv(csv_file)

df[["district", "city"]] = df["location"].str.split(", ", n=1, expand=True)
df["district"] = df["district"].str.replace("\n", "").str.strip().str.replace("·", "")
df = df.drop("location", axis=1)

df = df[
    [
        "prid",
        "title",
        "time_published",
        "district",
        "city",
        "price",
        "acreage",
        "price_per_m2",
        "bedrooms",
        "bathrooms",
        "product_url",
        "main_image",
        "description",
    ]
]

df["prid"] = df["prid"].astype("Int64")
df["title"] = df["title"].astype(str)
df["district"] = df["district"].astype(str)
df["city"] = df["city"].astype(str)
df["time_published"] = pd.to_datetime(df["time_published"]).dt.date
df["price"] = df["price"].apply(convert_price)
df["acreage"] = df["acreage"].apply(convert_acreage)
df["price_per_m2"] = df.apply(
    lambda row: int(round(row["price"] / row["acreage"])), axis=1
)
df["bedrooms"] = df["bedrooms"].astype("Int64")
df["bathrooms"] = df["bathrooms"].astype("Int64")
df["product_url"] = df["product_url"].astype(str)
df["main_image"] = df["main_image"].astype(str)
df["description"] = df["description"].astype(str)
df["source"] = "https://batdongsan.com.vn/"

db_file = os.path.join("demo_web", "data.db")

conn = sqlite3.connect(db_file)
df.to_sql(
    "products",
    conn,
    index=False,
    if_exists="replace",
    index_label="prid",
    dtype={"time_published": "DATE"},
)
conn.close()

print(f"Data from '{csv_file}' has been imported into SQLite database '{db_file}'.")
