# Car-recommendation-API

A RESTful API for exploring, searching and finding recommendations of used cars based on user preferences such as budget, mileage and vehicle attributes.

This project uses CI/CD and can be deployed to cloud platforms.

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
- **Backend**: FastAPI, Python 3.11
- **Server**: Uvicorn (ASGI)
- **Database**: PostgreSQL (production), SQLite (testing)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Auth**: API Key via `X-API-Key` header
- **Deployment**: Render (Docker)
- **CI/CD**: GitHub Actions + Render auto-deploy when CI succeeds

---

## Local Setup Two Options - Docker or Manual

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

To generate a secure API key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
#### 3. Download the dataset
Download `vehicles.csv` from [Kaggle](https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data/data) and place it in the `dataset/` folder so the path is:
```
dataset/vehicles.csv
```

#### 4. Import the dataset
```bash
python database/import_dataset.py
```

This imports up to 50,000 rows into the local SQLite database.

### 5. Build the Docker image
``` bash
docker build -t cars-api .
```

#### 6. Run the container
```bash
docker run -e API_KEY=your_key -e DATABASE_URL=sqlite:///cars.db -p 8000:8000 cars-api
```

API will be available at: http://localhost:8000
Swagger docs at: http://localhost:8000/docs

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

### 3. Install dependencies
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

Tests use a temporary SQLite database so it doesn't affect the actual PostgreSQL database. 19 tests are included.

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


### Backend
1. Create a new **Web Service** on [Render](https://render.com)
2. Connect your GitHub repository
3. Set runtime to **Docker** 
4. Add environment variables:
   - `API_KEY` — your generated API key
   - `DATABASE_URL` — your PostgreSQL connection string
5. Set auto-deploy to **After CI Checks Pass**
6. Deploy

### Frontend
1. Create a new **Static Site** on Render
2. Connect your GitHub repository
3. Set publish directory to `frontend`
4. Set auto-deploy to **After CI Checks Pass**
5. Deploy

## Project Structure
```
Car-recommendation-API/
├── app/
│   ├── __init__.py
│   ├── main.py              # Routes and business logic
│   ├── auth.py              # API key authentication
│   └── schemas.py           # Pydantic models
├── database/
│   ├── import_dataset.py    # Imports CSV into database
│   ├── verify_dataset.py    # Verifies import was successful
│   └── explore_dataset.py   # Explores raw CSV data
├── dataset/
│   └── vehicles.csv         # Not included, download from Kaggle
├── frontend/
│   ├── index.html
│   ├── search.html
│   ├── recommend.html
│   ├── stats.html
│   ├── similar.html
│   ├── car.html
│   ├── admin.html
│   ├── css/style.css
│   └── js/
│       └── admin.js
│       └── api.js
│       └── car.js
│       └── recommend.js
│       └── similar.js
│       └── stats.js
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_endpoints.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── .env                     # Not included, create manually
├── Dockerfile
├── requirements.txt
└── README.md