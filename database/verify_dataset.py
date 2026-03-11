from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///cars.db")

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