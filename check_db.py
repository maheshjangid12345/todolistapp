from app import create_app
from app.extensions import db
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    print("Tables in DB:", inspector.get_table_names())

