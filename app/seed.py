from werkzeug.security import generate_password_hash
from . import db
from .models import Category, Recipe, User

def seed_if_empty():
    if Category.query.count() == 0:
        for name in ["Deserti", "Hladna jela", "Finger food"]:
            db.session.add(Category(name=name))
        db.session.commit()

    if User.query.count() == 0:
        admin = User(
            username="admin",
            email="admin@example.com",
            password_hash=generate_password_hash("admin"),
            is_admin=True,
        )
        db.session.add(admin)
        db.session.commit()

    if Recipe.query.count() == 0:
        cats = {c.name: c for c in Category.query.all()}
        admin = User.query.filter_by(username="admin").first()

        r1 = Recipe(title="Primjer recept 1", summary="", instructions="", author_id=admin.id)
        r1.categories.append(cats["Deserti"])
        r2 = Recipe(title="Primjer recept 2", summary="", instructions="", author_id=admin.id)
        r2.categories.append(cats["Hladna jela"])
        r3 = Recipe(title="Primjer recept 3", summary="", instructions="", author_id=admin.id)
        r3.categories.append(cats["Finger food"])

        db.session.add_all([r1, r2, r3])
        db.session.commit()
