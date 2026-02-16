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
    return None

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)

    db_path = Path(app.config["DB_PATH"]).resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path.as_posix()

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    from .db_routes import db_bp
    app.register_blueprint(db_bp)

    return app
