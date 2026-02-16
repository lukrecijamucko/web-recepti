from flask import Blueprint, render_template
from .models import Category, Recipe

main_bp = Blueprint("main", __name__)

@main_bp.get("/")
def index():
    categories = Category.query.order_by(Category.id).limit(3).all()

    daily_picks = []
    for c in categories:
        recipe = (
            Recipe.query.join(Recipe.categories)
            .filter(Category.id == c.id)
            .order_by(Recipe.id)
            .first()
        )
        if recipe:
            daily_picks.append({"title": recipe.title, "category": c.name})

    return render_template("index.html", daily_picks=daily_picks)
