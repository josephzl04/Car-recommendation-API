from sqlalchemy import create_engine, text
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
engine = create_engine(f"sqlite:///{BASE_DIR /'cars.db'}")

with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM cars"))
    print("Rows in cars db:", result.scalar())

    sample = conn.execute(text("""
                               SELECT listing_id, manufacturer, model, year, price, fuel, transmission, odometer, body_type, state
                               FROM cars
                               LIMIT 10
                            """))
    
    print("\nSample rows:")
    for row in sample:
        print(row)

    result = conn.execute(text("PRAGMA table_info(cars)"))
    for row in result:
        print(row)