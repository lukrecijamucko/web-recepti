from flask import Blueprint
from . import db
from .seed import seed_if_empty

db_bp = Blueprint("db_bp", __name__, url_prefix="/db")

@db_bp.get("/init")
def init_db():
    db.create_all()
    seed_if_empty()
    return "DB OK"
