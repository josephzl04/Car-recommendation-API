#!/bin/sh
set -e

echo "Starting Car Recommendation API..."

# Only import the dataset if the database doesn't exist
if [ ! -f "cars.db" ]; then
  echo "cars.db not found."

  if [ ! -f "dataset/vehicles.csv" ]; then
    echo "Error: dataset/vehicles.csv not found."
    echo "Please download vehicles.csv from Kaggle and place it in the dataset folder before building the image."
    exit 1
  fi

  echo "Importing dataset..."
  python database/import_dataset.py
else
  echo "cars.db already exists. Skipping dataset import."
fi

echo "Launching API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8080