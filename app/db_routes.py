from flask import Blueprint, current_app
from sqlalchemy import text
from . import db
from .seed import seed_if_empty
from .models import Category, Recipe, User

db_bp = Blueprint("db_bp", __name__, url_prefix="/db")


@db_bp.get("/init")
def init_db():
    from . import models  

    db.create_all()
    seed_if_empty()

    rows = db.session.execute(
        text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    ).all()
    tables = [r[0] for r in rows]

    return (
        "DB OK\n"
        f"URI: {current_app.config.get('SQLALCHEMY_DATABASE_URI')}\n"
        f"TABLES: {tables}\n"
        f"counts: categories={Category.query.count()}, users={User.query.count()}, recipes={Recipe.query.count()}\n"
    )