from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from . import db
from .models import Recipe, Category

recipes_bp = Blueprint("recipes", __name__, url_prefix="/recipes")


@recipes_bp.get("/new")
@login_required
def new_recipe_form():
    categories = Category.query.order_by(Category.name).all()
    return render_template("recipe_new.html", categories=categories)


@recipes_bp.post("/new")
@login_required
def new_recipe_submit():
    title = (request.form.get("title") or "").strip()
    summary = (request.form.get("summary") or "").strip()
    ingredients = (request.form.get("ingredients") or "").strip()
    instructions = (request.form.get("instructions") or "").strip()

    category_ids = request.form.getlist("category_ids")  # više kategorija (M:N)

    if not title:
        flash("Naslov je obavezan.", "danger")
        return redirect(url_for("recipes.new_recipe_form"))
    if not ingredients:
        flash("Sastojci su obavezni.", "danger")
        return redirect(url_for("recipes.new_recipe_form"))
    if not instructions:
        flash("Upute su obavezne.", "danger")
        return redirect(url_for("recipes.new_recipe_form"))
    if not category_ids:
        flash("Odaberi barem jednu kategoriju.", "danger")
        return redirect(url_for("recipes.new_recipe_form"))

    recipe = Recipe(
        title=title,
        summary=summary,
        ingredients=ingredients,
        instructions=instructions,
        author_id=current_user.id,
    )

    categories = Category.query.filter(Category.id.in_(category_ids)).all()
    recipe.categories = categories

    db.session.add(recipe)
    db.session.commit()

    flash("Recept spremljen!", "success")
    return redirect(url_for("main.index"))

@recipes_bp.get("/")
def list_recipes():
    category_id = request.args.get("category", type=int)

    query = Recipe.query.order_by(Recipe.created_at.desc())

    if category_id:
        query = query.filter(Recipe.categories.any(id=category_id))

    recipes = query.all()
    categories = Category.query.order_by(Category.name).all()

    return render_template(
        "recipes_list.html",
        recipes=recipes,
        categories=categories,
        active_category=category_id,
    )

@recipes_bp.get("/<int:recipe_id>")
def recipe_detail(recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template("recipe_detail.html", recipe=recipe)