import pandas as pd
from sqlalchemy import create_engine

csv_path = "dataset/vehicles.csv"
db_path = "sqlite:///cars.db"

row_limit = 50000
chunk_size = 10000

columns_to_keep = [
    "id",
    "price",
    "year",
    "manufacturer",
    "model",
    "condition",
    "cylinders",
    "fuel",
    "odometer",
    "title_status",
    "transmission",
    "drive",
    "size",
    "type",
    "paint_color",
    "description",
    "state",
    "lat",
    "long",
    "posting_date",
]

engine = create_engine(db_path)

total_imported = 0
first_chunk = True

print("Loading dataset in chunks...")

for chunk in pd.read_csv(
    csv_path,
    usecols=columns_to_keep,
    chunksize=chunk_size,
    low_memory=False
):
    # clean numeric fields
    chunk["price"] = pd.to_numeric(chunk["price"], errors="coerce")
    chunk["year"] = pd.to_numeric(chunk["year"], errors="coerce")
    chunk["odometer"] = pd.to_numeric(chunk["odometer"], errors="coerce")

    # filter unrealistic values
    chunk = chunk[chunk["price"].between(500, 200000)]
    chunk = chunk[chunk["year"].between(1990, 2026)]
    chunk = chunk[chunk["odometer"].between(0, 500000)]

    # remove rows with missing key fields
    chunk = chunk.dropna(subset=[
        "price",
        "year",
        "manufacturer",
        "model",
        "fuel",
        "odometer",
        "transmission"
    ])
    
    chunk = chunk.drop_duplicates(subset=["id"])

    chunk = chunk.rename(columns={
        "id": "listing_id",
        "type": "body_type",
        "lat": "latitude",
        "long": "longitude"
    })

    # convert numeric to integer
    chunk["year"] = chunk["year"].astype(int)
    chunk["price"] = chunk["price"].astype(int)
    chunk["odometer"] = chunk["odometer"].astype(int)

    if row_limit is not None:
        remaining = row_limit - total_imported
        if remaining <= 0:
            break
        if len(chunk) > remaining:
            chunk = chunk.head(remaining)

    chunk.to_sql(
        "cars",
        engine,
        if_exists="replace" if first_chunk else "append",
        index=False
    )

    imported_now = len(chunk)
    total_imported += imported_now
    first_chunk = False

    print(f"Imported {total_imported} rows so far...")

    if row_limit is not None and total_imported >= row_limit:
        break

print("Import complete.")
print(f"Created database: cars.db")
print(f"Total imported rows: {total_imported}")