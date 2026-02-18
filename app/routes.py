from flask import Blueprint, render_template
from sqlalchemy import func
from .models import Category, Recipe

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    categories = Category.query.order_by(Category.id).limit(3).all()

    daily_picks = []
    for c in categories:
        r = (Recipe.query
             .join(Recipe.categories)
             .filter(Category.id == c.id)
             .order_by(func.random())
             .first())
        if r:
            daily_picks.append({"title": r.title, "category": c.name})

    return render_template("index.html", daily_picks=daily_picks)
