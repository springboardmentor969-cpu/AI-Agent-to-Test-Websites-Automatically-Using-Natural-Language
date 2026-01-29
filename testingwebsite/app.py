from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import requests
import os
from functools import wraps

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret"  # change in production

# ----------------- Database helpers -----------------
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
        g._database = db
    return db

def init_db():
    db = get_db()
    cur = db.cursor()
    # users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)
    # students table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        dept TEXT,
        grade TEXT
    )
    """)
    db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# call init_db when app starts
with app.app_context():
    init_db()

# ----------------- Authentication helpers -----------------
def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("You must be logged in to view that page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapped

def create_user(username, password):
    db = get_db()
    cur = db.cursor()
    pw_hash = generate_password_hash(password)
    try:
        cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, pw_hash))
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def verify_user(username, password):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    if row and check_password_hash(row["password_hash"], password):
        return row["id"]
    return None

# ----------------- Wikipedia helpers -----------------
WIKI_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

def fetch_random_wiki_article():
    headers = {"User-Agent": "FlaskApp/1.0 (contact: example@example.com)"}
    try:
        r = requests.get(WIKI_SUMMARY_URL, headers=headers, timeout=6)
        r.raise_for_status()
        data = r.json()
        title = data.get("title", "No Title")
        extract = data.get("extract", "")
        thumbnail = None
        if data.get("thumbnail") and data["thumbnail"].get("source"):
            thumbnail = data["thumbnail"]["source"]
        full_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
        return {"title": title, "extract": extract, "thumbnail": thumbnail, "url": full_url}
    except Exception as e:
        # return a harmless placeholder
        return {"title": "Could not fetch article", "extract": "Wikipedia may have blocked the request or network failed.", "thumbnail": None, "url": ""}

def get_multiple_random_articles(n=3):
    articles = []
    for _ in range(n):
        articles.append(fetch_random_wiki_article())
    return articles

# ----------------- Routes -----------------
@app.route("/", methods=["GET", "POST"])
def signup():
    # If user already logged in, redirect to dashboard
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")
        if not username or not password:
            flash("Please provide both username and password.", "danger")
            return render_template("signup.html")

        ok = create_user(username, password)
        if not ok:
            flash("Username already exists. Choose a different one.", "danger")
            return render_template("signup.html")
        flash("Account created. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")
        user_id = verify_user(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    username = session.get("username")
    articles = get_multiple_random_articles(3)
    return render_template("home.html", username=username, articles=articles)

# ----------------- Students CRUD -----------------
@app.route("/students", methods=["GET", "POST"])
@login_required
def students_page():
    db = get_db()
    cur = db.cursor()
    if request.method == "POST":
        sid = request.form.get("id").strip()
        name = request.form.get("name").strip()
        age = request.form.get("age")
        dept = request.form.get("dept").strip()
        grade = request.form.get("grade").strip()
        if not sid or not name:
            flash("ID and Name are required.", "danger")
            return redirect(url_for("students_page"))
        try:
            cur.execute("INSERT INTO students (id, name, age, dept, grade) VALUES (?, ?, ?, ?, ?)",
                        (sid, name, age if age else None, dept, grade))
            db.commit()
            flash("Student added.", "success")
        except sqlite3.IntegrityError:
            flash("A student with that ID already exists.", "danger")
        return redirect(url_for("students_page"))

    cur.execute("SELECT * FROM students ORDER BY name")
    rows = cur.fetchall()
    students = [dict(row) for row in rows]
    return render_template("students.html", students=students)

@app.route("/edit/<student_id>", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    db = get_db()
    cur = db.cursor()
    if request.method == "POST":
        # update
        name = request.form.get("name").strip()
        age = request.form.get("age")
        dept = request.form.get("dept").strip()
        grade = request.form.get("grade").strip()
        if not name:
            flash("Name is required.", "danger")
            return redirect(url_for("edit_student", student_id=student_id))
        cur.execute("UPDATE students SET name=?, age=?, dept=?, grade=? WHERE id=?", (name, age if age else None, dept, grade, student_id))
        db.commit()
        flash("Student updated.", "success")
        return redirect(url_for("students_page"))
    # GET
    cur.execute("SELECT * FROM students WHERE id=?", (student_id,))
    row = cur.fetchone()
    if row is None:
        flash("Student not found.", "danger")
        return redirect(url_for("students_page"))
    student = dict(row)
    return render_template("edit_student.html", student=student)

@app.route("/delete/<student_id>", methods=["POST"])
@login_required
def delete_student(student_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (student_id,))
    db.commit()
    flash("Student deleted.", "info")
    return redirect(url_for("students_page"))

# ----------------- Run -----------------
if __name__ == "__main__":
    # ensure DB exists
    with app.app_context():
        init_db()
    app.run(debug=True,port=5001)
