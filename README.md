# API Aggregator with FastAPI, Redis Cache & Authentication

This project is an **API aggregator** built with **FastAPI**, designed to fetch, combine, and serve data from multiple external APIs efficiently. It leverages **Redis** for caching responses to improve performance and reduce unnecessary external API calls, and it uses **JWT-based authentication** to secure access to endpoints. The application is fully asynchronous, ensuring fast response times even under high load.

## Features

- **FastAPI Framework**: A modern, high-performance Python web framework for building APIs.  
- **API Aggregation**: Fetches and combines data from multiple external sources into unified responses.  
- **Redis Caching**: Stores API responses in Redis to reduce redundant requests and improve response speed.  
- **Authentication & Security**: Token-based (JWT/OAuth2) authentication to protect endpoints.  
- **Async Support**: Asynchronous requests with HTTPX/aiohttp for efficient data fetching.

## Tech Stack

- **Python 3.13+**  
- **FastAPI** for the API backend  
- **Redis** for caching  
- **PostgreSQL** for database storage  
- **HTTPX / aiohttp** for async HTTP requests  
- **JWT / OAuth2** for authentication

## Environment Configuration

This project uses environment variables for database, cache, and authentication. A sample `.env.example` is provided:

### PostgreSQL

| Variable | Description |
|----------|-------------|
| `DB_USER` | PostgreSQL username |
| `DB_PASS` | PostgreSQL password |
| `DB_HOST` | PostgreSQL host (e.g., container name or localhost) |
| `DB_PORT` | PostgreSQL port (default: `5432`) |
| `DB_NAME` | PostgreSQL database name |

### Redis

| Variable | Description |
|----------|-------------|
| `REDIS_HOST` | Redis server host (e.g., container name or localhost) |
| `REDIS_PORT` | Redis server port (default: `6379`) |

### JWT Authentication

| Variable | Description |
|----------|-------------|
| `SECRET_KEY_FOR_JWT` | Secret key used to sign JWT tokens (change for production) |

# Quick Start

## Option 1: Run Locally with Python

```bash
# 1. Clone the repository
git clone https://github.com/rapid305/fastapi-redis-aggregator-jwt.git
cd fastapi-redis-aggregator-jwt

# 2. Copy environment file and edit if needed
cp .env.example .env
# (optional) Edit .env for PostgreSQL, Redis, and JWT settings

# 3. Install dependencies
pip install -r requirements.txt

# 4. Make sure Redis and PostgreSQL are running

# 5. Start the FastAPI server
uvicorn main:app --reload

# Access the API docs at: http://localhost:8000/docs

```

## Option 2: Run with Docker Compose
# Start the entire stack (FastAPI, Redis, PostgreSQL)

```bash

docker-compose up -d

# Stop the services
docker-compose down

# API will be available at: http://localhost:8000/docs

# Environment variables in .env control database, Redis, and JWT configuration.

# Responses from external APIs are cached automatically in Redis.
