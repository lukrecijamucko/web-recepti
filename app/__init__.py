import os
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: str):
    from .models import User
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)

    raw_db_path = app.config.get("DB_PATH", "app.db")
    raw_db_path = Path(raw_db_path)

    if raw_db_path.is_absolute():
        db_path = raw_db_path
    else:
        db_path = Path(app.instance_path) / raw_db_path  

    db_path.parent.mkdir(parents=True, exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path.as_posix()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from . import models  

    from .routes import main_bp
    app.register_blueprint(main_bp)

    from .db_routes import db_bp
    app.register_blueprint(db_bp)

    from .auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from .recipes_routes import recipes_bp
    app.register_blueprint(recipes_bp)

    return app
