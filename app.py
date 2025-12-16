from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)
from dotenv import load_dotenv
import os
import json
import csv
from datetime import datetime
from email_service import send_contact_email

# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# APP CONFIG
# --------------------------------------------------
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

# --------------------------------------------------
# CONTEXT PROCESSOR (for footer year)
# --------------------------------------------------
@app.context_processor
def inject_year():
    return {"datetime": datetime}

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def save_to_csv(name, email, message):
    os.makedirs("data", exist_ok=True)
    with open("data/messages.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name,
            email,
            message
        ])

def get_messages():
    messages = []
    try:
        with open("data/messages.csv", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                messages.append(row)
    except FileNotFoundError:
        pass

    # latest message first
    return messages[::-1]

# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------
@app.route("/")
def home():
    # Load projects
    try:
        with open("data/projects.json", "r", encoding="utf-8") as f:
            projects = json.load(f)
    except FileNotFoundError:
        projects = []

    skills = {
        "Languages": ["Python", "JavaScript"],
        "Frameworks": ["Flask"],
        "AI / Automation": ["NLP", "Speech Recognition", "Automation"],
        "Tools": ["Git", "GitHub", "VS Code"]
    }

    return render_template(
        "index.html",
        projects=projects,
        skills=skills
    )

# --------------------------------------------------
# RESUME PAGE
# --------------------------------------------------
@app.route("/resume-page")
def resume_page():
    return render_template("resume.html")

# --------------------------------------------------
# CONTACT FORM
# --------------------------------------------------
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not name or not email or not message:
        flash("All fields are required!", "error")
        return redirect(url_for("home"))

    # Save message
    save_to_csv(name, email, message)

    # Send email
    try:
        send_contact_email(name, email, message)
        flash("Message sent successfully!", "success")
    except Exception as e:
        print(e)
        flash("Message saved, but email failed.", "warning")

    return redirect(url_for("home"))

# --------------------------------------------------
# ADMIN LOGIN
# --------------------------------------------------
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if (
            username == os.getenv("ADMIN_USERNAME") and
            password == os.getenv("ADMIN_PASSWORD")
        ):
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid credentials", "error")

    return render_template("admin_login.html")

# --------------------------------------------------
# ADMIN DASHBOARD
# --------------------------------------------------
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    messages = get_messages()
    return render_template("admin_dashboard.html", messages=messages)

# --------------------------------------------------
# ADMIN LOGOUT
# --------------------------------------------------
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("home"))

# --------------------------------------------------
# RUN APP (LOCAL)
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

