from flask import Flask, render_template, request, url_for, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)


def connect_db():
    return sqlite3.connect("demo_web/data.db")


def format_date(date_str):
    if date_str is not None:
        date_object = datetime.strptime(date_str, "%Y-%m-%d")
        return date_object.strftime("%d-%m-%Y")
    else:
        return ""


def format_price(price):
    if price is not None:
        if price >= 1000000000:
            return f"{price / 1000000000:.2f} tỷ"
        else:
            return f"{price / 1000000:.2f} triệu"
    else:
        return ""


@app.route("/")
def all_products():
    connection = connect_db()
    cursor = connection.cursor()

    query = "SELECT prid, title, district, city, time_published, price, acreage, price_per_m2, bedrooms, bathrooms, product_url, main_image, description, source FROM products"
    cursor.execute(query)
    products = cursor.fetchall()

    formatted_products = []
    for product in products:
        formatted_product = list(product)
        formatted_product[4] = format_date(product[4])
        formatted_product[5] = format_price(product[5])
        formatted_product[7] = format_price(product[7])
        formatted_products.append(formatted_product)

    connection.close()

    return render_template("index.html", products=formatted_products, search_query="")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET" and "search_query" in request.args:
        return redirect(url_for("search", search_query=request.args["search_query"]))

    search_query = request.form.get("search_query", "")
    connection = connect_db()
    cursor = connection.cursor()

    query = f"SELECT prid, title, district, city, time_published, price, acreage, price_per_m2, bedrooms, bathrooms, product_url, main_image, description, source FROM products WHERE title LIKE '%{search_query}%'"
    cursor.execute(query)
    products = cursor.fetchall()

    formatted_products = []
    for product in products:
        formatted_product = list(product)
        formatted_product[4] = format_date(product[4])
        formatted_product[5] = format_price(product[5])
        formatted_product[7] = format_price(product[7])
        formatted_products.append(formatted_product)

    connection.close()

    return render_template(
        "index.html", products=formatted_products, search_query=search_query
    )


if __name__ == "__main__":
    app.run(debug=True)
