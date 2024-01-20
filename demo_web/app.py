from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def connect_db():
    return sqlite3.connect("test.db")


@app.route("/")
def index():
    connection = connect_db()
    cursor = connection.cursor()

    query = "SELECT prid, title, district, city, time_published, price, acreage, price_per_m2, bedrooms, bathrooms, product_url, main_image, description, source FROM products"
    cursor.execute(query)
    products = cursor.fetchall()

    connection.close()

    return render_template("index.html", products=products)


if __name__ == "__main__":
    app.run(debug=True)
