import os, uuid
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import config
from db import q

app = Flask(__name__)
app.config.from_object(config)

CATEGORIES = ["Classroom Facilities", "Laboratory Issues", "Library Issues", "Hostel Issues",
              "Washroom Maintenance", "Electricity Problems", "Drinking Water",
              "Internet/Wi-Fi Problems", "Other Issues"]
STATUSES = ["Submitted", "Under Review", "In Progress", "Resolved", "Rejected"]
DEPARTMENTS = ["Maintenance", "IT Department", "Library", "Hostel Office", "Electrical", "Academic Office"]
ALLOWED = {"png", "jpg", "jpeg", "gif"}


def login_required(role):
    def deco(f):
        @wraps(f)
        def wrapper(*a, **k):
            if session.get("role") != role:
                flash("Please log in to continue.", "warning")
                return redirect(url_for("login"))
            return f(*a, **k)
        return wrapper
    return deco


@app.route("/")
def home():
    if session.get("role") == "admin":
        return redirect(url_for("admin_dashboard"))
    if session.get("role") == "student":
        return redirect(url_for("student_dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        f = {k: request.form.get(k, "").strip() for k in ["name", "email", "roll_no", "department", "phone"]}
        pw, pw2 = request.form.get("password", ""), request.form.get("confirm", "")
        if not all([f["name"], f["email"], f["roll_no"], f["department"]]) or "@" not in f["email"]:
            flash("Please fill all required fields with a valid email.", "danger")
        elif len(pw) < 6:
            flash("Password must be at least 6 characters.", "danger")
        elif pw != pw2:
            flash("Passwords do not match.", "danger")
        elif q("SELECT id FROM students WHERE email=%s OR roll_no=%s", (f["email"].lower(), f["roll_no"]), one=True):
            flash("Email or roll number already registered.", "danger")
        else:
            q("INSERT INTO students (name,email,roll_no,department,phone,password_hash) VALUES (%s,%s,%s,%s,%s,%s)",
              (f["name"], f["email"].lower(), f["roll_no"], f["department"], f["phone"], generate_password_hash(pw)),
              commit=True)
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role", "student")
        table = "admins" if role == "admin" else "students"
        user = q(f"SELECT * FROM {table} WHERE email=%s", (request.form.get("email", "").strip().lower(),), one=True)
        if user and check_password_hash(user["password_hash"], request.form.get("password", "")):
            session.clear()
            session.update(user_id=user["id"], name=user["name"], role=role)
            return redirect(url_for("home"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# ---------------- Student ----------------
@app.route("/dashboard")
@login_required("student")
def student_dashboard():
    sid = session["user_id"]
    stats = q("""SELECT COUNT(*) total,
                 COALESCE(SUM(status IN ('Submitted','Under Review','In Progress')),0) pending,
                 COALESCE(SUM(status='Resolved'),0) resolved
                 FROM complaints WHERE student_id=%s""", (sid,), one=True)
    complaints = q("SELECT * FROM complaints WHERE student_id=%s ORDER BY created_at DESC", (sid,))
    anns = q("SELECT * FROM announcements ORDER BY created_at DESC LIMIT 3")
    return render_template("student_dashboard.html", stats=stats, complaints=complaints, anns=anns)


@app.route("/profile")
@login_required("student")
def profile():
    s = q("SELECT * FROM students WHERE id=%s", (session["user_id"],), one=True)
    return render_template("profile.html", s=s)


@app.route("/complaints/new", methods=["GET", "POST"])
@login_required("student")
def submit_complaint():
    if request.method == "POST":
        cat = request.form.get("category", "")
        title = request.form.get("title", "").strip()
        desc = request.form.get("description", "").strip()
        file = request.files.get("image")
        filename = None
        if cat not in CATEGORIES or not title or len(desc) < 10:
            flash("Choose a category, add a title and a description (10+ characters).", "danger")
            return render_template("submit_complaint.html", categories=CATEGORIES)
        if file and file.filename:
            ext = file.filename.rsplit(".", 1)[-1].lower()
            if ext not in ALLOWED:
                flash("Only PNG, JPG, JPEG or GIF images are allowed.", "danger")
                return render_template("submit_complaint.html", categories=CATEGORIES)
            filename = uuid.uuid4().hex + "." + ext
            file.save(os.path.join(config.UPLOAD_FOLDER, secure_filename(filename)))
        q("INSERT INTO complaints (student_id,category,title,description,image) VALUES (%s,%s,%s,%s,%s)",
          (session["user_id"], cat, title, desc, filename), commit=True)
        flash("Complaint submitted successfully.", "success")
        return redirect(url_for("student_dashboard"))
    return render_template("submit_complaint.html", categories=CATEGORIES)


# ---------------- Admin ----------------
@app.route("/admin")
@login_required("admin")
def admin_dashboard():
    stats = q("""SELECT COUNT(*) total,
                 COALESCE(SUM(status IN ('Submitted','Under Review')),0) pending,
                 COALESCE(SUM(status='In Progress'),0) in_progress,
                 COALESCE(SUM(status='Resolved'),0) resolved FROM complaints""", one=True)
    students = q("SELECT COUNT(*) n FROM students", one=True)["n"]
    by_status = {r["status"]: r["n"] for r in q("SELECT status, COUNT(*) n FROM complaints GROUP BY status")}
    counts = [by_status.get(s, 0) for s in STATUSES]
    recent = q("""SELECT c.*, s.name student FROM complaints c JOIN students s ON s.id=c.student_id
                  ORDER BY c.created_at DESC LIMIT 5""")
    return render_template("admin_dashboard.html", stats=stats, students=students,
                           statuses=STATUSES, counts=counts, recent=recent)


@app.route("/admin/complaints")
@login_required("admin")
def manage_complaints():
    search = request.args.get("q", "").strip()
    status = request.args.get("status", "")
    cat = request.args.get("category", "")
    sql = "SELECT c.*, s.name student, s.roll_no FROM complaints c JOIN students s ON s.id=c.student_id WHERE 1=1"
    params = []
    if search:
        sql += " AND (c.title LIKE %s OR s.name LIKE %s OR s.roll_no LIKE %s)"
        params += [f"%{search}%"] * 3
    if status in STATUSES:
        sql += " AND c.status=%s"; params.append(status)
    if cat in CATEGORIES:
        sql += " AND c.category=%s"; params.append(cat)
    rows = q(sql + " ORDER BY c.created_at DESC", tuple(params))
    return render_template("manage_complaints.html", rows=rows, statuses=STATUSES, categories=CATEGORIES,
                           departments=DEPARTMENTS, search=search, status=status, cat=cat)


@app.route("/admin/complaints/<int:cid>/update", methods=["POST"])
@login_required("admin")
def update_complaint(cid):
    status = request.form.get("status")
    dept = request.form.get("department") or None
    if status in STATUSES and (dept is None or dept in DEPARTMENTS):
        q("UPDATE complaints SET status=%s, department=%s WHERE id=%s", (status, dept, cid), commit=True)
        flash("Complaint updated.", "success")
    else:
        flash("Invalid status or department.", "danger")
    return redirect(request.referrer or url_for("manage_complaints"))


@app.route("/admin/students")
@login_required("admin")
def students_list():
    rows = q("""SELECT s.*, (SELECT COUNT(*) FROM complaints c WHERE c.student_id=s.id) complaints
                FROM students s ORDER BY s.created_at DESC""")
    return render_template("students.html", rows=rows)


# ---------------- Announcements ----------------
@app.route("/announcements", methods=["GET", "POST"])
def announcements():
    if session.get("role") not in ("admin", "student"):
        return redirect(url_for("login"))
    if request.method == "POST":
        if session["role"] != "admin":
            return redirect(url_for("login"))
        t, d = request.form.get("title", "").strip(), request.form.get("description", "").strip()
        if t and d:
            q("INSERT INTO announcements (admin_id,title,description) VALUES (%s,%s,%s)",
              (session["user_id"], t, d), commit=True)
            flash("Announcement published.", "success")
        else:
            flash("Title and description are required.", "danger")
        return redirect(url_for("announcements"))
    rows = q("SELECT * FROM announcements ORDER BY created_at DESC")
    return render_template("announcements.html", rows=rows)


@app.route("/announcements/<int:aid>/delete", methods=["POST"])
@login_required("admin")
def delete_announcement(aid):
    q("DELETE FROM announcements WHERE id=%s", (aid,), commit=True)
    flash("Announcement deleted.", "info")
    return redirect(url_for("announcements"))


@app.errorhandler(404)
def not_found(e):
    return render_template("login.html"), 404


@app.errorhandler(413)
def too_large(e):
    flash("Image too large (max 2 MB).", "danger")
    return redirect(url_for("submit_complaint"))


if __name__ == "__main__":
    app.run(debug=True)
