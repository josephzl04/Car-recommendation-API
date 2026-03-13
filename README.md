# Car-recommendation-API

A RESTful API for exploring, searching and finding recommendations of used cars based on user preferences such as budget, mileage and vehicle attributes.

The system uses a public dataset of used car listings to allow users to query vehicles, analyse market trends.

The API is built using FastAPI, and deployed using Docker with CI/CD automation.

## Features

### Core API functionality
- Create, read, update, and delete car listings
- Retrieve individual cars by ID
- Search cars with filters
- Recommend cars based on user preferences
- Find similar vehicles
- Market analytics and statistics

## Live Deployed Links
- **API**: https://car-recommendation-api.onrender.com
- **API Docs**: https://car-recommendation-api.onrender.com/docs
- **Frontend**: https://car-recommendation-frontend.onrender.com

## Tech Stack
- **Backend**: FastAPI, Python 3.11, Uvicorn (ASGI Server)
- **Database**: PostgreSQL (production), SQLite (local development and testing)
- **ORM**: SQLAlchemy ORM
- **Validation**: Pydantic
- **Authentication**: API Key via `X-API-Key` header
- **Deployment**: Render (Docker containerisation)
- **CI/CD**: GitHub Actions + Render auto-deploy when CI succeeds

## Dataset
This project uses the Craigslist Vehicles Dataset from Kaggle:
https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data
The dataset contains vehicle listings with attributes such as:
- Manufacturer
- Model
- Price
- Year
- Mileage
- Fuel type

To ensure manageable local development and faster queries, the dataset python import script loads up to 50,000 rows into the database.

## Authentication
The API is protected using an API Key

Requests must include the following header:
X-API-Key: your_secret_key_here

Requests without a valid key will return:
401 Unauthorised


## API Documentation
Interactive API documentation is automatically generated using FastAPI Swagger.
It includes full endpoint definitions, request parameters, and example responses.

Access the live interactive documentation here:
https://car-recommendation-api.onrender.com/docs

A static PDF version of the API documentation is also included in this  repository:

[API Documentation PDF](/APIdoc.pdf)

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|------|------|------|:------:|
| GET | `/` | Check that the API is running | ❌ |
| GET | `/cars` | Retrieve a list of cars (supports `limit` query parameter) | ❌ |
| GET | `/cars/{listing_id}` | Retrieve a single car by its listing ID | ❌ |
| GET | `/cars/search` | Search for cars using filters such as manufacturer, price, year, fuel, mileage, etc. | ❌ |
| GET | `/cars/recommend` | Recommend cars based on budget, mileage, and preference scoring | ❌ |
| GET | `/cars/similar/{listing_id}` | Find vehicles similar to a given car listing | ❌ |
| POST | `/cars` | Create a new car listing | ✅ |
| PUT | `/cars/{listing_id}` | Update an existing car listing | ✅ |
| DELETE | `/cars/{listing_id}` | Delete a car listing | ✅ |
| GET | `/admin/test` | Test endpoint to verify API key authentication | ✅ |
| GET | `/stats` | General market statistics and overview | ❌ |
| GET | `/stats/price-trends` | Average car price trends by year | ❌ |
| GET | `/stats/market-insights` | Market insights such as affordable manufacturers and value states | ❌ |

---

## Local Setup
Two options are available
Docker
Manual Python environment

### Prerequisites
- Python 3.11 or Docker
- Git

### Option 1: Docker
Requires Docker to be installed.

#### 1. Clone the repository
```bash
git clone https://github.com/josephzl04/Car-recommendation-API.git
cd Car-recommendation-API
```

#### 2. Set up environment variables
Create a `.env` file in the project root:
```
API_KEY=your_secret_key_here
DATABASE_URL=sqlite:///cars.db
```

#### 3. Download the dataset
Download `vehicles.csv` from [Kaggle](https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data/data) and place it in the `dataset/` folder so the path is:
```
dataset/vehicles.csv
```

This imports up to 50,000 rows into the local SQLite database.

#### 5. Build the Docker image
Make sure to open Docker Desktop
``` bash
docker build -t cars-api .
```

#### 6. Run the container
```bash
docker run -e API_KEY=your_key -e DATABASE_URL=sqlite:///cars.db -p 8080:8080 cars-api
```

API will be available at: http://localhost:8080
Swagger docs at: http://localhost:8080/docs

> Note: Docker handles starting the local server automatically - no need to run uvicorn manually.

---

### Option 2: Manual Setup

#### 1. Clone the repository
```bash
git clone https://github.com/josephzl04/Car-recommendation-API.git
cd Car-recommendation-API
```

#### 2. Create a virtual environment
```bash
python -m venv venv
```

Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate 
# Mac/Linux      
source venv/bin/activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Download the dataset
Download `vehicles.csv` from [Kaggle](https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data/data) and place it in the `dataset/` folder so the path is:
```
dataset/vehicles.csv
```

#### 5. Set up environment variables
Create a `.env` file in the project root:
```
API_KEY=your_secret_key_here
DATABASE_URL=sqlite:///cars.db
```

To generate a secure API key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

#### 6. Import the dataset
```bash
python database/import_dataset.py
```

This imports up to 50,000 rows into the local SQLite database.

#### 7. Run the API
```bash
uvicorn app.main:app --reload
```

API will be available at: http://localhost:8000  
Swagger docs at: http://localhost:8000/docs

---

## Running Tests
```bash
pytest tests/ -v
```

Tests use a temporary SQLite database so it doesn't affect the actual database. 19 tests are included.

---

## CI/CD Pipeline

### Continuous Integration (Github Actions)
Every push to main branch automatically runs the full python tests through GitHub Actions.
The workflow is defined in '.github/workflows/ci.yml'.
Test results are visible in the **Actions** tab on GitHub.

### Continuous Deployment (Render)
Both the backend and frontend are configured to auto deploy on Render after CI checks pass. This ensures that broken code is never deployed live.

---

## Deployment (Render)

### Database (PostgreSQL)
1. Create a new **PostgreSQL** instance on Render
2. Copy the **External Database URL**
3. Import the dataset pointing to the Render database:
```bash
# Windows
set DATABASE_URL=your_render_db_url && python database/import_dataset.py

# Mac/Linux
DATABASE_URL=your_render_db_url python database/import_dataset.py
```

### Backend Deployment
1. Create a new **Web Service** on [Render](https://render.com)
2. Connect your GitHub repository
3. Set runtime to **Docker** 
4. Add environment variables:
   - `API_KEY` — your generated API key
   - `DATABASE_URL` — your PostgreSQL connection string
5. Set auto-deploy to **After CI Checks Pass**
6. Deploy

### Frontend Deployment
1. Create a new **Static Site** on Render
2. Connect your GitHub repository
3. Set publish directory to `frontend`
4. Set auto-deploy to **After CI Checks Pass**
5. Deploy