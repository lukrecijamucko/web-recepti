import os
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
    except (ValueError, TypeError):
        return None

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    from pathlib import Path
    db_path = Path(app.config["DB_PATH"]).resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path.as_posix()

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import main_bp
    from .db_routes import db_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(db_bp)

    with app.app_context():
        from .seed import seed_if_empty
        db.create_all()
        seed_if_empty()

    return app
