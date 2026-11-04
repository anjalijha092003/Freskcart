
from flask import Flask, render_template, request, jsonify
import sqlite3
import json
import os
from datetime import datetime

app = Flask(__name__)

# Custom Jinja filter for JSON
app.jinja_env.filters['from_json'] = json.loads

# Database path
DB = os.path.join(os.path.dirname(__file__), "freshcart.db")

# Grocery Products
PRODUCTS = [
    {"id": 1, "name": "Fresh Apples", "category": "Fruits", "price": 120, "unit": "kg", "emoji": "🍎", "tag": "Fresh"},
    {"id": 2, "name": "Bananas", "category": "Fruits", "price": 60, "unit": "dozen", "emoji": "🍌", "tag": "Popular"},
    {"id": 3, "name": "Sweet Oranges", "category": "Fruits", "price": 90, "unit": "kg", "emoji": "🍊", "tag": "Seasonal"},
    {"id": 4, "name": "Farm Carrots", "category": "Vegetables", "price": 45, "unit": "kg", "emoji": "🥕", "tag": "Organic"},
    {"id": 5, "name": "Green Broccoli", "category": "Vegetables", "price": 80, "unit": "piece", "emoji": "🥦", "tag": "Fresh"},
    {"id": 6, "name": "Tomatoes", "category": "Vegetables", "price": 35, "unit": "kg", "emoji": "🍅", "tag": "Daily"},
    {"id": 7, "name": "Whole Milk", "category": "Dairy", "price": 60, "unit": "L", "emoji": "🥛", "tag": "Dairy"},
    {"id": 8, "name": "Brown Bread", "category": "Bakery", "price": 45, "unit": "pack", "emoji": "🍞", "tag": "Baked"},
    {"id": 9, "name": "Basmati Rice", "category": "Groceries", "price": 95, "unit": "kg", "emoji": "🍚", "tag": "Pantry"},
    {"id": 10, "name": "Farm Eggs", "category": "Dairy", "price": 85, "unit": "6 pcs", "emoji": "🥚", "tag": "Protein"},
    {"id": 11, "name": "Fresh Spinach", "category": "Vegetables", "price": 30, "unit": "bunch", "emoji": "🥬", "tag": "Healthy"},
    {"id": 12, "name": "Strawberries", "category": "Fruits", "price": 160, "unit": "box", "emoji": "🍓", "tag": "Treat"}
]


# Initialize Database
def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer TEXT,
                phone TEXT,
                address TEXT,
                items TEXT,
                total REAL,
                created_at TEXT
            )
        """)


init_db()


# Home Page
@app.route("/")
def home():
    return render_template("index.html", products=PRODUCTS)


# Place Order API
@app.route("/api/order", methods=["POST"])
def create_order():
    data = request.get_json(silent=True) or {}

    customer = data.get("customer", "").strip()
    phone = data.get("phone", "").strip()
    address = data.get("address", "").strip()
    items = data.get("items", [])

    if not customer or not phone or not address or not items:
        return jsonify({
            "error": "Please fill all details and add products."
        }), 400

    total = 0
    clean = []

    for item in items:
        try:
            product_id = int(item.get("id", 0))
            qty = max(1, int(item.get("qty", 1)))
        except (ValueError, TypeError):
            continue

        product = next(
            (p for p in PRODUCTS if p["id"] == product_id),
            None
        )

        if product:
            clean.append({
                "id": product["id"],
                "name": product["name"],
                "qty": qty,
                "price": product["price"]
            })

            total += product["price"] * qty

    if not clean:
        return jsonify({
            "error": "No valid products in cart."
        }), 400

    with sqlite3.connect(DB) as con:
        cur = con.execute("""
            INSERT INTO orders
            (customer, phone, address, items, total, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            customer,
            phone,
            address,
            json.dumps(clean),
            total,
            datetime.now().strftime("%d-%m-%Y %I:%M %p")
        ))

        order_id = cur.lastrowid

    return jsonify({
        "message": "Order placed successfully!",
        "order_id": order_id,
        "total": total
    })


# Admin Orders Dashboard
@app.route("/admin")
def admin():
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row

        orders = con.execute("""
            SELECT * FROM orders
            ORDER BY id DESC
        """).fetchall()

    return render_template("admin.html", orders=orders)


# Run Application
if __name__ == "__main__":
    app.run(debug=True)
