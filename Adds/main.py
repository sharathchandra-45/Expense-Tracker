from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# --- Create database and tables ---
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    # expenses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        category TEXT,
        amount TEXT,
        date TEXT
    )
    """)


    conn.commit()
    conn.close()

init_db()

# --- LOGIN PAGE ---
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect("/home")
        else:
            return "Invalid username or password! Try again."

    return render_template("login.html")

# --- REGISTER PAGE ---
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("register.html")

# --- HOME PAGE ---
@app.route("/home")
def home():
    return render_template("home.html")

# --- MAIN PAGE (Expenses) ---
@app.route("/main", methods=["GET", "POST"])
def main():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]
        date = request.form["date"]

        cursor.execute("INSERT INTO expenses (title, amount, date) VALUES (?, ?, ?)",
                       (title, amount, date))
        conn.commit()

    cursor.execute("SELECT * FROM expenses")
    data = cursor.fetchall()
    conn.close()

    return render_template("main.html", expenses=data)

# --- ABOUT PAGE ---
@app.route("/about")
def about():
    return render_template("about.html")

# --- CONTACT PAGE ---
@app.route("/contact")
def contact():
    return render_template("contact.html")

# --- CATEGORY PAGE ---
@app.route("/category/<cat>", methods=["GET", "POST"])
def category_page(cat):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]
        date = request.form["date"]

        cursor.execute(
            "INSERT INTO expenses (title, category, amount, date) VALUES (?, ?, ?, ?)",
            (title, cat, amount, date)
        )
        conn.commit()

    cursor.execute("SELECT * FROM expenses WHERE category=?", (cat,))
    data = cursor.fetchall()
    conn.close()

    return render_template("category.html", expenses=data, category=cat)


# --- RUN APP ---
if __name__ == "__main__":
    app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True)
