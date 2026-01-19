from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from agent import run_agent
from playwright_executor import PlaywrightExecutor
from reporting_module import ReportingModule, TestStatus
from dom_mapper import AdvancedErrorHandler

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
    commands = []
    assertions = []
    generated_code = None

    if request.method == "POST":
        user_input = request.form.get("instruction", "").strip()
        if user_input:
            state = run_agent(user_input)
            result = state.get("response", "")
            actions = state.get("actions", [])
            commands = state.get("commands", [])
            assertions = state.get("assertions", [])
            generated_code = state.get("generated_code", "")

    return render_template("agent.html", 
                         result=result, 
                         actions=actions,
                         commands=commands,
                         assertions=assertions,
                         generated_code=generated_code)


@app.route("/execute", methods=["POST", "OPTIONS"])
def execute_test():
    """Execute generated Playwright test code with reporting."""
    # Handle CORS preflight
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response
    
    start_time = datetime.now()
    reporting = ReportingModule()
    error_handler = AdvancedErrorHandler()
    
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
            if data.get("code"):
                import json
                data = json.loads(data.get("code", "{}"))
        
        code = data.get("code", "")
        test_name = data.get("test_name", "test_automated")
        instruction = data.get("instruction", "")
        commands = data.get("commands", [])
        
        if not code:
            response = jsonify({
                "success": False,
                "error": "No code provided",
                "status": "error"
            })
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400
        
        executor = PlaywrightExecutor()
        result = executor.execute_test(code, test_name)
        
        # Enhance error message if there's an error
        if result.get("error"):
            error_context = {
                "selector": "N/A",
                "page_url": "N/A"
            }
            enhanced_error = error_handler.enhance_error_message(
                result.get("error", ""),
                error_context
            )
            result["enhanced_error"] = enhanced_error
            result["error_type"], result["recovery_suggestion"] = error_handler.classify_error(
                result.get("error", "")
            )
        
        # Create and save report
        try:
            report = reporting.create_report(
                test_name=test_name,
                instruction=instruction or "Automated test",
                generated_code=code,
                execution_result=result,
                commands=commands,
                start_time=start_time
            )
            report_path = reporting.save_report(report)
            result["report_id"] = report.test_id
            result["report_path"] = report_path
            result["report_html"] = reporting.format_report_html(report)
            result["report_json"] = reporting.format_report_json(report)
        except Exception as report_error:
            # Don't fail execution if reporting fails
            result["report_error"] = str(report_error)
        
        response = jsonify(result)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        enhanced_error = error_handler.enhance_error_message(str(e), {})
        
        response = jsonify({
            "success": False,
            "error": str(e),
            "enhanced_error": enhanced_error,
            "error_details": error_details,
            "status": "error"
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500


@app.route("/install-browsers", methods=["POST"])
def install_browsers():
    """Install Playwright browsers."""
    try:
        executor = PlaywrightExecutor()
        result = executor.install_browsers()
        
        response = jsonify(result)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
        
    except Exception as e:
        response = jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500


@app.route("/validate-code", methods=["POST"])
def validate_code():
    """Validate generated code syntax."""
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        code = data.get("code", "")
        
        if not code:
            response = jsonify({
                "valid": False,
                "errors": ["No code provided"]
            })
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400
        
        executor = PlaywrightExecutor()
        result = executor.validate_code(code)
        
        response = jsonify(result)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
        
    except Exception as e:
        response = jsonify({
            "valid": False,
            "errors": [str(e)]
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "message": "Server is running",
        "endpoints": {
            "execute": "/execute",
            "validate": "/validate-code",
            "agent": "/agent",
            "reports": "/reports"
        }
    })


@app.route("/reports", methods=["GET"])
def get_reports():
    """Get recent test reports."""
    try:
        reporting = ReportingModule()
        limit = request.args.get("limit", 10, type=int)
        reports = reporting.get_recent_reports(limit=limit)
        
        response = jsonify({
            "success": True,
            "reports": reports,
            "count": len(reports)
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    except Exception as e:
        response = jsonify({
            "success": False,
            "error": str(e)
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500


@app.route("/report/<report_id>", methods=["GET"])
def get_report(report_id):
    """Get specific test report."""
    try:
        import json
        reporting = ReportingModule()
        report_file = os.path.join(reporting.reports_dir, f"{report_id}.json")
        
        if not os.path.exists(report_file):
            return jsonify({"error": "Report not found"}), 404
        
        with open(report_file, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
        
        response = jsonify({
            "success": True,
            "report": report_data
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    except Exception as e:
        response = jsonify({
            "success": False,
            "error": str(e)
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500


@app.route("/download-report/<report_id>", methods=["GET"])
def download_report(report_id):
    """Download test report in JSON or HTML format."""
    try:
        import json
        from flask import send_file, make_response
        
        reporting = ReportingModule()
        report_file = os.path.join(reporting.reports_dir, f"{report_id}.json")
        
        if not os.path.exists(report_file):
            return jsonify({"error": "Report not found"}), 404
        
        with open(report_file, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
        
        format_type = request.args.get("format", "json").lower()
        
        if format_type == "html":
            # Convert report data back to TestReport object for HTML formatting
            from reporting_module import TestReport, TestStep, TestStatus
            from datetime import datetime
            
            # Reconstruct TestReport object
            steps = [
                TestStep(
                    step_number=s.get("step_number", 0),
                    description=s.get("description", ""),
                    action_type=s.get("action_type", ""),
                    target=s.get("target"),
                    status=TestStatus(s.get("status", "passed")),
                    duration=s.get("duration", 0.0)
                )
                for s in report_data.get("steps", [])
            ]
            
            report = TestReport(
                test_id=report_data.get("test_id", ""),
                test_name=report_data.get("test_name", ""),
                instruction=report_data.get("instruction", ""),
                status=TestStatus(report_data.get("status", "passed")),
                start_time=datetime.fromisoformat(report_data.get("start_time", "")),
                end_time=datetime.fromisoformat(report_data.get("end_time", "")) if report_data.get("end_time") else None,
                duration=report_data.get("duration", 0.0),
                total_steps=report_data.get("total_steps", 0),
                passed_steps=report_data.get("passed_steps", 0),
                failed_steps=report_data.get("failed_steps", 0),
                steps=steps,
                assertions_passed=report_data.get("assertions_passed", 0),
                assertions_failed=report_data.get("assertions_failed", 0),
                error_message=report_data.get("error_message"),
                output_log=report_data.get("output_log"),
                error_log=report_data.get("error_log"),
                generated_code=report_data.get("generated_code"),
                browser_info=report_data.get("browser_info")
            )
            
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Report - {report.test_name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .report-container {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
    </style>
</head>
<body>
    {reporting.format_report_html(report)}
</body>
</html>"""
            
            response = make_response(html_content)
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            response.headers['Content-Disposition'] = f'attachment; filename=test_report_{report_id}.html'
            return response
        
        else:  # JSON format
            response = make_response(json.dumps(report_data, indent=2, ensure_ascii=False))
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            response.headers['Content-Disposition'] = f'attachment; filename=test_report_{report_id}.json'
            return response
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/reports-view")
def reports_view():
    """View all test reports."""
    reporting = ReportingModule()
    reports = reporting.get_recent_reports(limit=50)
    return render_template("reports.html", reports=reports)


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
