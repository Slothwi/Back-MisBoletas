import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from app.db.session import engine

def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT @@VERSION"))
        print("Conexión exitosa. Versión del servidor:")
        for row in result:
            print(row[0])

if __name__ == "__main__":
    test_connection()