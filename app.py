from flask import Flask, render_template, request, redirect, url_for, send_file, session
from flask_mysqldb import MySQL
import pandas as pd


app = Flask(__name__)

app.secret_key = "grocery_secret_key"


# -----------------------------
# MySQL Configuration
# -----------------------------

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root123"
app.config["MYSQL_DB"] = "grocery_db"


mysql = MySQL(app)



# -----------------------------
# Home
# -----------------------------

@app.route("/")
def home():

    return render_template("index.html")





# -----------------------------
# Products
# -----------------------------

@app.route("/products")
def products():

    search = request.args.get("search", "")

    cursor = mysql.connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM products

        WHERE name LIKE %s
        OR category LIKE %s

        """,
        (
            "%" + search + "%",
            "%" + search + "%"
        )
    )


    products = cursor.fetchall()


    cursor.close()


    return render_template(
        "products.html",
        products=products,
        search=search
    )





# -----------------------------
# Add Product
# -----------------------------

@app.route("/add_product", methods=["GET","POST"])
def add_product():

    cursor = mysql.connection.cursor()


    if request.method == "POST":


        name = request.form["name"]

        category = request.form["category"]

        price = request.form["price"]

        quantity = request.form["quantity"]



        cursor.execute(
            """
            INSERT INTO products
            (
            name,
            category,
            price,
            quantity
            )

            VALUES
            (%s,%s,%s,%s)

            """,
            (
                name,
                category,
                price,
                quantity
            )
        )


        mysql.connection.commit()


        cursor.close()


        return redirect(
            url_for("products")
        )


    cursor.close()


    return render_template(
        "add_product.html"
    )





# -----------------------------
# Edit Product
# -----------------------------

@app.route("/edit_product/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    cursor = mysql.connection.cursor()

    if request.method == "POST":

        name = request.form["name"]

        category = request.form["category"]

        price = request.form["price"]

        quantity = request.form["quantity"]

        cursor.execute(
            """
            UPDATE products
            SET
                name=%s,
                category=%s,
                price=%s,
                quantity=%s
            WHERE id=%s
            """,
            (name, category, price, quantity, id)
        )

        mysql.connection.commit()

        cursor.close()

        return redirect(url_for("products"))

    cursor.execute(
        "SELECT * FROM products WHERE id=%s",
        (id,)
    )

    product = cursor.fetchone()

    cursor.close()

    return render_template(
        "edit_product.html",
        product=product
    )





# -----------------------------
# Delete Product
# -----------------------------

@app.route("/delete_product/<int:id>")
def delete_product(id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    cursor.close()

    return redirect(url_for("products"))





# -----------------------------
# Dashboard
# -----------------------------

@app.route("/dashboard")
def dashboard():

    cursor = mysql.connection.cursor()



    # Total Products

    cursor.execute(
        "SELECT COUNT(*) FROM products"
    )

    total_products = cursor.fetchone()[0]




    # Total Customers

    cursor.execute(
        "SELECT COUNT(*) FROM customers"
    )

    total_customers = cursor.fetchone()[0]




    # Total Orders

    cursor.execute(
        "SELECT COUNT(*) FROM orders"
    )

    total_orders = cursor.fetchone()[0]




    # Total Sales

    cursor.execute(
        "SELECT SUM(total_price) FROM orders"
    )

    total_sales = cursor.fetchone()[0]


    if total_sales is None:
        total_sales = 0





    # Low Stock Count

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM products
        WHERE quantity < 10
        """
    )


    low_stock = cursor.fetchone()[0]






    # Sales Chart Data

    cursor.execute(
        """
        SELECT

        products.name,
        SUM(orders.quantity)


        FROM orders


        INNER JOIN products

        ON orders.product_id = products.id


        GROUP BY products.name


        ORDER BY SUM(orders.quantity) DESC

        """
    )


    sales_data = cursor.fetchall()






    # Recent Orders

    cursor.execute(
        """
        SELECT

        orders.id,
        customers.name,
        products.name,
        orders.quantity,
        orders.total_price,
        orders.order_date


        FROM orders


        INNER JOIN customers

        ON orders.customer_id = customers.id


        INNER JOIN products

        ON orders.product_id = products.id


        ORDER BY orders.id DESC


        LIMIT 5

        """
    )


    recent_orders = cursor.fetchall()





    # Low Stock Products

    cursor.execute(
        """
        SELECT

        id,
        name,
        quantity


        FROM products


        WHERE quantity < 10


        ORDER BY quantity ASC

        """
    )


    low_stock_products = cursor.fetchall()



    cursor.close()



    return render_template(
        "dashboard.html",

        total_products=total_products,

        total_customers=total_customers,

        total_orders=total_orders,

        total_sales=total_sales,

        low_stock=low_stock,

        sales_data=sales_data,

        recent_orders=recent_orders,

        low_stock_products=low_stock_products

    )








# -----------------------------
# Customers
# -----------------------------

@app.route("/customers")
def customers():

    search = request.args.get("search", "")

    cursor = mysql.connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM customers

        WHERE name LIKE %s
        OR phone LIKE %s
        OR email LIKE %s

        """,
        (
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"
        )
    )


    customers = cursor.fetchall()


    cursor.close()


    return render_template(
        "customers.html",
        customers=customers,
        search=search
    )





# -----------------------------
# Add Customer
# -----------------------------

@app.route("/add_customer", methods=["GET", "POST"])
def add_customer():

    if request.method == "POST":

        name = request.form["name"]

        phone = request.form["phone"]

        email = request.form["email"]

        address = request.form["address"]

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            INSERT INTO customers
            (
                name,
                phone,
                email,
                address
            )
            VALUES
            (%s,%s,%s,%s)
            """,
            (
                name,
                phone,
                email,
                address
            )
        )

        mysql.connection.commit()

        cursor.close()

        return redirect(
            url_for("customers")
        )

    return render_template(
        "add_customer.html"
    )





# -----------------------------
# Edit Customer
# -----------------------------

@app.route("/edit_customer/<int:id>", methods=["GET","POST"])
def edit_customer(id):

    cursor = mysql.connection.cursor()

    if request.method == "POST":

        name = request.form["name"]

        phone = request.form["phone"]

        email = request.form["email"]

        address = request.form["address"]

        cursor.execute(
            """
            UPDATE customers
            SET
            name=%s,
            phone=%s,
            email=%s,
            address=%s
            WHERE id=%s
            """,
            (
                name,
                phone,
                email,
                address,
                id
            )
        )

        mysql.connection.commit()

        cursor.close()

        return redirect(
            url_for("customers")
        )

    cursor.execute(
        "SELECT * FROM customers WHERE id=%s",
        (id,)
    )

    customer = cursor.fetchone()

    cursor.close()

    return render_template(
        "edit_customer.html",
        customer=customer
    )





# -----------------------------
# Delete Customer
# -----------------------------

@app.route("/delete_customer/<int:id>")
def delete_customer(id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM customers WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    cursor.close()

    return redirect(
        url_for("customers")
    )








# -----------------------------
# Orders
# -----------------------------

@app.route("/orders")
def orders():

    cursor = mysql.connection.cursor()


    cursor.execute(
        """
        SELECT

        orders.id,
        customers.name,
        products.name,
        orders.quantity,
        orders.total_price,
        orders.order_date


        FROM orders


        INNER JOIN customers

        ON orders.customer_id = customers.id


        INNER JOIN products

        ON orders.product_id = products.id


        ORDER BY orders.id DESC

        """
    )


    orders = cursor.fetchall()


    cursor.close()


    return render_template(
        "orders.html",
        orders=orders
    )








# -----------------------------
# Add Order
# -----------------------------

@app.route("/add_order", methods=["GET","POST"])
def add_order():

    cursor = mysql.connection.cursor()



    cursor.execute(
        "SELECT * FROM customers"
    )


    customers = cursor.fetchall()




    cursor.execute(
        """
        SELECT *
        FROM products
        WHERE quantity > 0
        """
    )


    products = cursor.fetchall()




    if request.method == "POST":


        customer_id = request.form["customer_id"]

        product_id = request.form["product_id"]

        quantity = int(request.form["quantity"])




        cursor.execute(
            """
            SELECT price, quantity
            FROM products
            WHERE id=%s

            """,
            (product_id,)
        )


        product = cursor.fetchone()



        price = product[0]

        stock = product[1]




        if quantity > stock:

            cursor.close()

            return "Not enough stock"




        total_price = price * quantity




        cursor.execute(
            """
            INSERT INTO orders
            (
            customer_id,
            product_id,
            quantity,
            total_price,
            order_date
            )

            VALUES
            (%s,%s,%s,%s,CURDATE())

            """,
            (
                customer_id,
                product_id,
                quantity,
                total_price
            )
        )





        cursor.execute(
            """
            UPDATE products

            SET quantity = quantity - %s

            WHERE id=%s

            """,
            (
                quantity,
                product_id
            )
        )



        mysql.connection.commit()


        cursor.close()



        return redirect(
            url_for("orders")
        )




    cursor.close()


    return render_template(
        "add_order.html",
        customers=customers,
        products=products
    )






# -----------------------------
# Export Orders
# -----------------------------

@app.route("/export_orders")
def export_orders():

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT

        orders.id,
        customers.name,
        products.name,
        orders.quantity,
        orders.total_price,
        orders.order_date


        FROM orders


        INNER JOIN customers

        ON orders.customer_id = customers.id


        INNER JOIN products

        ON orders.product_id = products.id

        """
    )

    data = cursor.fetchall()

    cursor.close()

    df = pd.DataFrame(
        data,
        columns=[
            "Order ID",
            "Customer",
            "Product",
            "Quantity",
            "Total Price",
            "Order Date"
        ]
    )

    file_name = "orders_report.xlsx"

    df.to_excel(file_name, index=False)

    return send_file(
        file_name,
        as_attachment=True
    )





# -----------------------------
# Login
# -----------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()

        cursor.close()

        if user:

            session["username"] = username

            return redirect("/")

        else:

            return "Invalid Username or Password"

    return render_template("login.html")





# -----------------------------
# Logout
# -----------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")





# -----------------------------
# Register
# -----------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()

        cursor.execute(
            "INSERT INTO users(username, password) VALUES(%s,%s)",
            (username, password)
        )

        mysql.connection.commit()

        cursor.close()

        return redirect("/login")

    return render_template("register.html")





# -----------------------------
# Run Application
# -----------------------------

if __name__ == "__main__":

    app.run(debug=True)