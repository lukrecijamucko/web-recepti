from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

@main_bp.get("/")
def index():
    daily_picks = [
        {"title": "Primjer recept 1", "category": "Deserti"},
        {"title": "Primjer recept 2", "category": "Hladna jela"},
        {"title": "Primjer recept 3", "category": "Finger food"},
    ]
    return render_template("index.html", daily_picks=daily_picks)
