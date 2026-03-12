from sqlalchemy import create_engine, text
#from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

#BASE_DIR = Path(__file__).resolve().parent.parent
#engine = create_engine(f"sqlite:///{BASE_DIR /'cars.db'}")

engine = create_engine(os.getenv("DATABASE_URL"))
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

   # result = conn.execute(text("PRAGMA table_info(cars)"))
   # for row in result:
   #     print(row)