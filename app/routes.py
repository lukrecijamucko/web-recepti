from flask import Blueprint, render_template, current_app
from flask_login import login_required
from sqlalchemy import func
from sqlalchemy.exc import OperationalError

from .models import Category, Recipe

main_bp = Blueprint("main", __name__)


@main_bp.get("/me")
@login_required
def me():
    return render_template("profile.html")


@main_bp.get("/")
def index():
    daily_picks = []

    try:
        categories = Category.query.order_by(Category.id).limit(3).all()

        for c in categories:
            r = (
                Recipe.query
                .filter(Recipe.categories.any(id=c.id))
                .order_by(func.random())
                .first()
            )
            if r:
                daily_picks.append({"id": r.id, "title": r.title, "category": c.name})

    except OperationalError:
        pass

    return render_template(
        "index.html",
        daily_picks=daily_picks,
        db_uri=current_app.config.get("SQLALCHEMY_DATABASE_URI"),
    )