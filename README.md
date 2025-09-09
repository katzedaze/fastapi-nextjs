# FastAPI Next.js Full-Stack Application

test
test2
This is a full-stack web application template using FastAPI for the backend, Next.js for the frontend, and PostgreSQL with pgvector for the database. The project is containerized with Docker for both development and production environments.

## Project Structure

```
├── backend                  # FastAPI application
│   ├── alembic              # Database migrations
│   ├── app
│   │   ├── api              # API endpoints
│   │   ├── core             # Core functionality
│   │   ├── db               # Database session and models
│   │   ├── models           # SQLAlchemy models
│   │   ├── schemas          # Pydantic schemas
│   │   ├── services         # Business logic services
│   │   └── tests            # Unit and integration tests
│   └── scripts
│       └── seeders          # Database seeders
├── frontend                 # Next.js application
│   ├── public               # Static files
│   └── src
│       ├── app              # Next.js App Router
│       ├── components       # React components
│       ├── contexts         # React contexts
│       ├── hooks            # Custom React hooks
│       ├── lib              # Utility functions
│       ├── services         # API services
│       ├── types            # TypeScript type definitions
│       └── utils            # Helper utilities
└── nginx                    # Nginx configuration for production
```

## Technologies Used

### Backend

- **FastAPI**: Modern, fast web framework for building APIs
- **Poetry**: Python dependency management
- **Pydantic**: Data validation and settings management
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool
- **PostgreSQL**: Relational database
- **pgvector**: Vector similarity search extension for PostgreSQL

### Frontend

- **Next.js**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Re-usable UI components built with Radix UI and Tailwind CSS

### Infrastructure

- **Docker**: Containerization
- **Nginx**: Web server for production environment

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Make (optional, but recommended)

### Setup

#### Using Make (Recommended)

This project includes a Makefile to simplify Docker operations.

1. Clone the repository

   ```bash
   git clone https://github.com/yourusername/fastapi-nextjs.git
   cd fastapi-nextjs
   ```

2. Set up the environment (creates .env file from example)

   ```bash
   make setup
   ```

3. Build and start the development environment

   ```bash
   make build
   make up
   ```

4. Run database migrations

   ```bash
   make migrate
   ```

5. Seed the database (optional)

   ```bash
   make seed
   ```

#### Using Docker Compose Directly

1. Clone the repository

   ```bash
   git clone https://github.com/yourusername/fastapi-nextjs.git
   cd fastapi-nextjs
   ```

2. Create environment files

   ```bash
   cp .env.example .env
   cp frontend/.env.local.example frontend/.env.local
   ```

3. Start the development environment

   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

4. Run database migrations

   ```bash
   docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head
   ```

5. Seed the database (optional)

   ```bash
   docker-compose -f docker-compose.dev.yml exec backend python -m scripts.seed
   ```

### Accessing the Applications

- Frontend: <http://localhost:3000>
- Backend API: <http://localhost:8000/api/v1>
- API Documentation: <http://localhost:8000/docs>

## Development

### Makefile Commands

For convenience, the project includes a Makefile with the following commands:

```bash
# Show available commands
make help

# Environment options: ENV=dev (default) or ENV=prod
make <command> ENV=dev|prod

# Setup environment (.env files)
make setup

# Build services
make build

# Start services in detached mode
make up

# Stop and remove services
make down

# Restart services
make restart

# Show running containers
make ps

# Show logs
make logs

# Run database migrations
make migrate

# Run migrations step by step
make migrate-step

# Seed the database (all tables)
make seed

# Seed specific tables
make seed-users
make seed-items
make seed-orders

# Reset database, run migrations and seed (reliable method)
make seed-all

# Access shell in backend container
make shell

# Access PostgreSQL in database container
make shell-db

# Clean up everything (remove containers, volumes, networks)
make clean
```

### Backend Development

The backend is built with FastAPI and follows a modular structure:

- **API Routes**: Define API endpoints in `backend/app/api`
- **Models**: Define SQLAlchemy models in `backend/app/models`
- **Schemas**: Define Pydantic schemas in `backend/app/schemas`
- **Services**: Implement business logic in `backend/app/services`
- **Database**: Manage database connections in `backend/app/db`

#### Creating Migrations

After making changes to the models, create a new migration:

```bash
make shell
alembic revision --autogenerate -m "description"
exit
```

Apply the migration:

```bash
make migrate
```

#### Running Tests

```bash
docker-compose -f docker-compose.dev.yml exec backend pytest
```

### Frontend Development

The frontend is built with Next.js 14 using the App Router and follows a component-based structure:

- **Pages**: Define pages in `frontend/src/app`
- **Components**: Create reusable components in `frontend/src/components`
- **API Services**: Implement API services in `frontend/src/services`
- **Hooks**: Create custom hooks in `frontend/src/hooks`
- **Context**: Manage application state in `frontend/src/contexts`

## Production Deployment

To deploy the application in production:

1. Ensure SSL certificates are available in `nginx/ssl/cert.pem` and `nginx/ssl/key.pem`

2. Start the production environment using Make:

   ```bash
   make setup ENV=prod
   make up ENV=prod
   make migrate ENV=prod
   make seed ENV=prod  # Optional
   ```

   Or using Docker Compose directly:

   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
   docker-compose -f docker-compose.prod.yml exec backend python -m scripts.seed  # Optional
   ```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
