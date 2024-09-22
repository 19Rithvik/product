import sqlite3
from pydantic import BaseModel
from fastapi import FastAPI,HTTPException

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float
    quantity: int
    description: str = None
    category: str = None

def db_connection():
    return sqlite3.connect('products.db')

def create_table():
    conn = db_connection()
    conn.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL CHECK(price > 0),
        quantity INTEGER NOT NULL CHECK(quantity >= 0),
        description TEXT,
        category TEXT
        );
     """)

    conn.commit()
    conn.close()

create_table()

def insert_initial_products():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products")
    cursor.executemany("""
        INSERT INTO products (name, price, quantity, description, category) VALUES (?, ?, ?, ?, ?)
    """, [
        ("Wireless Bluetooth Headphones", 79.99, 50, "Noise-cancelling over-ear headphones with 30-hour battery life.", "Electronics"),
        ("Organic Green Tea", 12.99, 200, "100% organic green tea leaves, packed for freshness.", "Beverages"),
        ("Yoga Mat", 29.99, 150, "Non-slip, eco-friendly yoga mat for all types of workouts.", "Fitness"),
        ("Stainless Steel Water Bottle", 19.99, 75, "Double-wall insulated water bottle, keeps drinks cold for 24 hours.", "Outdoor"),
        ("Smart LED Desk Lamp", 39.99, 60, "Touch control lamp with adjustable brightness and color temperature.", "Home"),
        ("Wireless Charging Pad", 24.99, 100, "Fast wireless charging compatible with most smartphones.", "Accessories"),
        ("Bluetooth Fitness Tracker", 49.99, 80, "Tracks heart rate, steps, and sleep patterns with smartphone connectivity.", "Wearables"),
    ])
    conn.commit()
    conn.close()


insert_initial_products()


@app.post("/products")
def create_product(product : Product):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price, quantity, description, category) VALUES (?,?,?,?,?)",(product.name,product.price,product.quantity,product.description,product.category)
    )
    conn.commit()
    prod_id = cursor.lastrowid
    conn.close()
    return {"id": prod_id , **product.dict()}

@app.get("/products/{product_id}")
def get_product(product_id : int):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?",(product_id,))
    conn.commit()
    product = cursor.fetchone()
    conn.close()
    if product is None:
            raise HTTPException(status_code=404, detail="No data found")
    
    return {"id": product[0] , "name": product[1], "price": product[2], "quantity": product[3], "description": product[4], "category": product[5]}

@app.get("/products")
def list_products(min_val : float):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE price >= ?",(min_val,))
    conn.commit()
    list_products = cursor.fetchall()
    conn.close()
    return [{"id": product[0] , "name": product[1], "price": product[2], "quantity": product[3], "description": product[4], "category": product[5]} for product in list_products]

@app.put("/products/{product_id}")
def update_product(product_id : int,product: Product):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET UPDATE products SET name=?, price=?, quantity=?, description=?, category=? WHERE id=?""", 
                    (product.name, product.price, product.quantity, product.description, product.category, product_id))

    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="No data found")

    conn.close()
    return {"id": product_id , **product.dict()}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?",(product_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="No data found")
    
    conn.close()
    return {"deatail": "product is deleted"}