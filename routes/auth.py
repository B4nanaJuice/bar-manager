from flask import Blueprint, render_template, request, redirect, url_for, session
import os

page = Blueprint("auth", __name__, template_folder = "templates", static_folder = "static", url_prefix = "/auth")

@page.route("/login", methods = ["GET", "POST"])
def login():
    if 'user' in session and session['user'] == os.getenv("ADMIN_USERNAME"):
        return redirect(url_for('admin.admin_panel'))
    
    if request.method == "POST":
        # Get login information
        username: str = request.form.get("username") or None
        password: str = request.form.get("password") or None

        # Check login information
        if not username or not password:
            return redirect(url_for('public.cocktails'))
        
        if username != os.getenv("ADMIN_USERNAME") or password != os.getenv("ADMIN_PASSWORD"):
            return redirect(url_for('public.cocktails'))
        
        session["user"] = os.getenv("ADMIN_USERNAME")

        return redirect(url_for('admin.admin_panel'))

    return render_template("login.html.jinja", page_title = "Authentification")