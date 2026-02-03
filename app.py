from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Avdya@7468",
    database="user_db"
)
cursor = conn.cursor(dictionary=True)

#  HOME / LOGIN PAGE
@app.route("/")
def index():   
    return render_template("index.html")

@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        try:
            cursor.execute(
                "INSERT INTO users (fullname, email, username, password) VALUES (%s, %s, %s, %s)",
                (fullname, email, username, hashed_password)
            )
            conn.commit()
            flash("Registration successful! Please login.")
            return redirect(url_for("index"))

        except mysql.connector.IntegrityError:
            flash("Username or email already exists!")
            return redirect(url_for("register"))

    return render_template("register.html")


# LOGIN FORM (POST) 
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user["password"], password):
        flash("Login successful!")
        return f"Welcome, {user['fullname']}"
    else:
        flash("Invalid username or password!")
        return redirect(url_for("index"))

#  RUN APP
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

