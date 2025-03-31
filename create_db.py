# create_db.py
from app.db import engine, create_tables

create_tables()

print("=============Tables created successfully============")