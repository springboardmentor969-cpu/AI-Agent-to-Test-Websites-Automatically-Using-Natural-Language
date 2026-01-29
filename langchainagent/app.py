from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from agent import run_agent

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'auth.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User {self.username}>'

# Create tables
with app.app_context():
    db.create_all()
    
    # Add default users if they don't exist
    if User.query.filter_by(username="admin").first() is None:
        admin = User(username="admin", password="1234", email="admin@example.com")
        db.session.add(admin)
    
    if User.query.filter_by(username="user").first() is None:
        user = User(username="user", password="password123", email="user@example.com")
        db.session.add(user)
    
    db.session.commit()

# Dummy user database (you can replace with real DB later)
users = {
    "admin": "1234",
    "user": "password123"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session["user"] = username
            user.last_login = datetime.utcnow()
            db.session.commit()
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        email = request.form.get("email", "")

        if not username or not password:
            return render_template("signup.html", error="Username and password are required")
        
        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match")
        
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            return render_template("signup.html", error="Username already exists")
        
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("signup.html")


# ---------------- FORGOT PASSWORD ----------------
@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        username = request.form.get("username", "")
        user = User.query.filter_by(username=username).first()

        if user:
            return render_template("forgot.html", message="Password reset link sent to your email!")
        else:
            return render_template("forgot.html", error="User not found.")

    return render_template("forgot.html")


# ---------------- MAIN DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    
    user = User.query.filter_by(username=session["user"]).first()
    if not user:
        return redirect(url_for("login"))
    
    return render_template("dashboard.html", user=user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/agent", methods=["GET", "POST"])
def agent_view():
    """Handle natural language instructions via the LangGraph agent."""
    result = None
    actions = []

    if request.method == "POST":
        user_input = request.form.get("instruction", "").strip()
        if user_input:
            state = run_agent(user_input)
            result = state.get("response", "")
            actions = state.get("actions", [])

    return render_template("agent.html", result=result, actions=actions)


@app.route("/testpage")
def testpage():
    """Static page used by automated Playwright tests."""
    return render_template("testpage.html")


@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("login"))
    
    user = User.query.filter_by(username=session["user"]).first()
    if not user:
        return redirect(url_for("login"))
    
    return render_template("profile.html", user=user)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
