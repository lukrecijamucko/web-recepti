from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from . import db
from .models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password_hash, password):
            flash("Krivi username ili lozinka.")
            return render_template("auth_login.html")

        login_user(user)
        return redirect(url_for("main.index"))

    return render_template("auth_login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("Sva polja su obavezna.")
            return render_template("auth_register.html")

        if User.query.filter_by(username=username).first() is not None:
            flash("Username je zauzet.")
            return render_template("auth_register.html")

        if User.query.filter_by(email=email).first() is not None:
            flash("Email je već registriran.")
            return render_template("auth_register.html")

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=False,
        )
        db.session.add(user)
        db.session.commit()

        flash("Račun je napravljen. Sad se prijavi.")
        return redirect(url_for("auth.login"))

    return render_template("auth_register.html")


@auth_bp.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
