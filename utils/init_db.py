from dotenv import load_dotenv
load_dotenv()

import os
print("Текущий DATABASE_URL:", os.environ.get("DATABASE_URL"))

from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
    print("Все таблицы успешно созданы!") 