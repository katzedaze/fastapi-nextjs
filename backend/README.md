# FastAPI Backend

This is the backend API for the FastAPI-NextJS application.

## Technology Stack

- **FastAPI**: Fast, modern API framework for Python
- **SQLAlchemy**: Object-relational mapper (ORM)
- **Pydantic**: Data validation and settings management
- **Alembic**: Database migration tool
- **Poetry**: Dependency management
- **PostgreSQL**: Relational database
- **pg-vector**: Vector similarity search extension for PostgreSQL

## Project Structure

```
backend/
├── alembic/            # Database migrations
├── app/
│   ├── api/            # API endpoints
│   │   └── api_v1/     # API version 1
│   ├── core/           # Core functionality
│   ├── db/             # Database session and models
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic services
│   └── tests/          # Unit and integration tests
└── scripts/
    └── seeders/        # Database seeders
```

## Development

### Local Setup

1. Install dependencies:
   ```bash
   cd backend
   pip install poetry
   poetry install
   ```

2. Run the server:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

### SQLAlchemy Enums

This project uses SQLAlchemy enums for database models:

```python
class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(Base, BaseModel):
    # ...
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    # ...
```

When using these enums in database operations, always use the enum value (e.g., `OrderStatus.PENDING`) rather than the string value ("pending").

### Seed Data

Run the seeder script:
```bash
python -m scripts.seed
```

To run individual seeders:
```bash
python scripts/run_seeder.py [user|item|order]
```

## API Documentation

- API documentation is available at `/docs` when the server is running.
- OpenAPI schema is available at `/openapi.json`.

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```
# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=app
POSTGRES_PORT=5432

# Backend Configuration
PROJECT_NAME="FastAPI-NextJS Application"
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=11520  # 8 days

# System Configuration
TZ=Asia/Tokyo
```