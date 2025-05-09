# Makefile for FastAPI-NextJS application

# Default environment (development)
ENV ?= dev

# Docker compose files
DC_DEV = docker-compose.dev.yml
DC_PROD = docker-compose.prod.yml

# Docker compose command based on environment
ifeq ($(ENV),dev)
	DC_FILE = $(DC_DEV)
else ifeq ($(ENV),prod)
	DC_FILE = $(DC_PROD)
endif

# Colors for terminal output
BLUE = \033[0;34m
GREEN = \033[0;32m
YELLOW = \033[0;33m
RED = \033[0;31m
NC = \033[0m # No Color

.PHONY: help setup build up down restart ps logs migrate seed seed-users seed-items seed-orders shell clean reset-db migrate-step seed-all

# Help command
help:
	@echo "${BLUE}FastAPI-NextJS Docker Management Commands${NC}"
	@echo "${YELLOW}Usage:${NC}"
	@echo "  make <command> [ENV=dev|prod]"
	@echo ""
	@echo "${YELLOW}Environment:${NC}"
	@echo "  ENV=dev       Development environment (default)"
	@echo "  ENV=prod      Production environment"
	@echo ""
	@echo "${YELLOW}Commands:${NC}"
	@echo "  ${GREEN}help${NC}        Show this help message"
	@echo "  ${GREEN}setup${NC}       Create .env file from example if it doesn't exist"
	@echo "  ${GREEN}build${NC}       Build or rebuild all services"
	@echo "  ${GREEN}up${NC}          Create and start all services in detached mode"
	@echo "  ${GREEN}down${NC}        Stop and remove all services"
	@echo "  ${GREEN}restart${NC}     Restart all services"
	@echo "  ${GREEN}ps${NC}          List running containers"
	@echo "  ${GREEN}logs${NC}        View output from containers"
	@echo "  ${GREEN}migrate${NC}     Run all database migrations"
	@echo "  ${GREEN}migrate-step${NC} Run migrations step by step"
	@echo "  ${GREEN}seed${NC}        Run all database seeders"
	@echo "  ${GREEN}seed-users${NC}  Seed only users table"
	@echo "  ${GREEN}seed-items${NC}  Seed only items table"
	@echo "  ${GREEN}seed-orders${NC} Seed only orders table"
	@echo "  ${GREEN}seed-all${NC}    Reset database, run migrations and seed incrementally"
	@echo "  ${GREEN}reset-db${NC}    Reset the database"
	@echo "  ${GREEN}shell${NC}       Access shell in backend container"
	@echo "  ${GREEN}shell-db${NC}    Access PostgreSQL in database container"
	@echo "  ${GREEN}clean${NC}       Remove all containers, volumes and networks"
	@echo ""
	@echo "${YELLOW}Examples:${NC}"
	@echo "  make setup ENV=dev      # Set up development environment"
	@echo "  make up ENV=dev         # Start development environment"
	@echo "  make seed-all ENV=dev   # Reset DB, run migrations, and seed the database"

# Setup command to create .env file and frontend .env.local if they don't exist
setup:
	@echo "${BLUE}Setting up $(ENV) environment...${NC}"
	@if [ ! -f .env ]; then \
		echo "${YELLOW}Creating .env file from example...${NC}"; \
		cp .env.example .env; \
	else \
		echo "${YELLOW}.env file already exists.${NC}"; \
	fi
	@if [ ! -f frontend/.env.local ]; then \
		echo "${YELLOW}Creating frontend/.env.local file from example...${NC}"; \
		if [ ! -d frontend ]; then mkdir -p frontend; fi; \
		cp frontend/.env.local.example frontend/.env.local 2>/dev/null || echo "${RED}No frontend/.env.local.example file.${NC}"; \
	else \
		echo "${YELLOW}frontend/.env.local file already exists.${NC}"; \
	fi
	@echo "${GREEN}Setup complete!${NC}"

# Build services
build:
	@echo "${BLUE}Building $(ENV) environment...${NC}"
	docker-compose -f $(DC_FILE) build

# Start services in detached mode
up:
	@echo "${BLUE}Starting $(ENV) environment...${NC}"
	docker-compose -f $(DC_FILE) up -d
	@echo "${GREEN}Services are running.${NC}"
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@if [ "$(ENV)" = "prod" ]; then \
		echo "Application: http://localhost"; \
	fi

# Stop and remove services
down:
	@echo "${BLUE}Stopping $(ENV) environment...${NC}"
	docker-compose -f $(DC_FILE) down
	@echo "${GREEN}Services have been stopped.${NC}"

# Restart services
restart:
	@echo "${BLUE}Restarting $(ENV) environment...${NC}"
	docker-compose -f $(DC_FILE) restart
	@echo "${GREEN}Services have been restarted.${NC}"

# Show running containers
ps:
	@echo "${BLUE}Current running containers in $(ENV) environment:${NC}"
	docker-compose -f $(DC_FILE) ps

# Show logs
logs:
	@echo "${BLUE}Showing logs for $(ENV) environment:${NC}"
	docker-compose -f $(DC_FILE) logs -f

# Reset database
reset-db:
	@echo "${BLUE}Resetting database in $(ENV) environment...${NC}"
	docker-compose -f $(DC_FILE) exec db psql -U postgres -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	@echo "${GREEN}Database reset complete!${NC}"

# Run all migrations
migrate:
	@echo "${BLUE}Running all database migrations in $(ENV) environment...${NC}"
	docker-compose -f $(DC_FILE) exec backend alembic upgrade head
	@echo "${GREEN}All migrations complete!${NC}"

# Run migrations step by step
migrate-step:
	@echo "${BLUE}Running migrations step by step in $(ENV) environment...${NC}"
	docker-compose -f $(DC_FILE) exec backend alembic upgrade 01_create_users
	@echo "${GREEN}Step 1: Users table migration complete!${NC}"
	docker-compose -f $(DC_FILE) exec backend alembic upgrade 02_create_items
	@echo "${GREEN}Step 2: Items table migration complete!${NC}"
	docker-compose -f $(DC_FILE) exec backend alembic upgrade 03_create_orders
	@echo "${GREEN}Step 3: Orders table migration complete!${NC}"
	docker-compose -f $(DC_FILE) exec backend alembic upgrade 04_create_order_items
	@echo "${GREEN}Step 4: Order-Items relationship migration complete!${NC}"
	@echo "${GREEN}All migrations complete!${NC}"

# Run user seeder only
seed-users:
	@echo "${BLUE}Seeding users in $(ENV) environment...${NC}"
	docker-compose -f $(DC_FILE) exec backend python scripts/run_seeder.py user
	@echo "${GREEN}User seeding complete!${NC}"

# Run item seeder only
seed-items:
	@echo "${BLUE}Seeding items in $(ENV) environment...${NC}"
	docker-compose -f $(DC_FILE) exec backend python scripts/run_seeder.py item
	@echo "${GREEN}Item seeding complete!${NC}"

# Run order seeder only
seed-orders:
	@echo "${BLUE}Seeding orders in $(ENV) environment...${NC}"
	docker-compose -f $(DC_FILE) exec backend python scripts/run_seeder.py order
	@echo "${GREEN}Order seeding complete!${NC}"

# Run all seeders
seed: seed-users seed-items seed-orders
	@echo "${GREEN}All seeding complete!${NC}"

# Reset database, run migrations and seed with incremental steps
seed-all: reset-db
	@echo "${BLUE}Starting incremental database setup in $(ENV) environment...${NC}"
	# Step 1: Create users table
	docker-compose -f $(DC_FILE) exec backend alembic upgrade 01_create_users
	@echo "${GREEN}Step 1: Users table migration complete!${NC}"
	# Step 2: Create items table
	docker-compose -f $(DC_FILE) exec backend alembic upgrade 02_create_items
	@echo "${GREEN}Step 2: Items table migration complete!${NC}"
	# Step 3: Create orders table
	docker-compose -f $(DC_FILE) exec backend alembic upgrade 03_create_orders
	@echo "${GREEN}Step 3: Orders table migration complete!${NC}"
	# Step 4: Create order_items table
	docker-compose -f $(DC_FILE) exec backend alembic upgrade 04_create_order_items
	@echo "${GREEN}Step 4: Order-Items relationship migration complete!${NC}"
	@echo "${GREEN}All migrations complete!${NC}"

	# Now run all seeders through the main script to ensure relationships are handled properly
	@echo "${BLUE}Running seeders...${NC}"
	docker-compose -f $(DC_FILE) exec backend python -m scripts.seed
	@echo "${GREEN}Database reset, migrations, and seeding all completed successfully!${NC}"

# Access shell in backend container
shell:
	@echo "${BLUE}Opening shell in backend container...${NC}"
	docker-compose -f $(DC_FILE) exec backend /bin/bash

# Access PostgreSQL in database container
shell-db:
	@echo "${BLUE}Opening PostgreSQL shell in database container...${NC}"
	docker-compose -f $(DC_FILE) exec db psql -U $${POSTGRES_USER:-postgres} -d $${POSTGRES_DB:-app}

# Clean up everything
clean:
	@echo "${RED}Stopping all containers and removing volumes...${NC}"
	docker-compose -f $(DC_DEV) down -v
	docker-compose -f $(DC_PROD) down -v
	@echo "${GREEN}Cleanup complete!${NC}"