# Wolfia - Design system interview - Implement an impersonation system

## Overview

This repository is designed to test your technical competence and coding skills by implementing an impersonation system. The goal is to allow internal users (e.g., admins) to impersonate other users, which is crucial for debugging issues and assisting with support requests.

## Task Description

### Requirements

1. **Initiate Impersonation**
    - Internal users (admins) should be able to impersonate any other user.
    - The system should create a new session for the impersonated user, linked to the admin initiating the impersonation.

2. **Impersonation Indicator**
    - The UI should clearly indicate when an admin is impersonating another user.
    - The system should allow the admin to stop impersonation and return to their own session.

3. **Access Control**
    - Only internal users (admins) can initiate impersonation.
    - The system should verify the permissions of the admin before allowing impersonation.

4. **Logging and Auditing**
    - Log all impersonation activities, including the admin initiating the impersonation, the impersonated user, and timestamps.

## Getting Started with Development

### Prerequisites

- Docker
- Docker Compose

## Installation

Run the following command to start all services using Docker Compose:

```sh
docker compose up --build
```

This command builds and starts all services defined in docker-compose.yml, setting up the frontend, backend, and database automatically. The backend will be available on http://localhost:2020, and the frontend will be on http://localhost:3000.

Note: You need to run this command from the root directory of the project where the `docker-compose.yml` file is located.

### 4. Initial Database Setup

On the first run, or whenever you need to update your database schema, run the Alembic migrations to create or update database tables:

```sh
docker compose exec backend alembic upgrade head
```

This command executes Alembic migrations inside the running backend container, ensuring your database schema is up-to-date.

## Start up the application

For subsequent runs, you can start the application using the following command:

```sh
docker compose up
```

## Project Structure

The project is divided into two main components: the frontend and the backend.

### Frontend

The frontend is a React application created using Create React App. It is a simple application that allows users to log in and see the user information. The goal is to see the impersonation feature in action here such that when you log in as an admin, you can impersonate other users and display their information.

### Backend

This contains the endpoints and database models for the application. The backend is using FastAPI to expose the endpoints and SQLAlchemy to interact with the database. The database is a PostgreSQL database running in a Docker container.

We already have the login and user endpoints set up in the backend. You can use the existing endpoints to implement the impersonation feature. Primarily, the login.py and user.py files contain the logic for authentication.

### Database

We use psql as the database for this project. The database is running in a Docker container and is accessible on port 5432. The database schema is managed using Alembic, which is a lightweight database migration tool for SQLAlchemy.

You can connect to the database using the following command:

```sh
docker compose exec db pgcli postgres://admin:admin_password@db:5432/interview
```

And then query the DB using psql.

## Setup for the project

Once you have everything set up, you can start working on the project. You should probably create a couple of users. You can do that by visiting the following URL:

```sh
http://localhost:3000/login
```

You can click on the register here button to create a new user. For internal users, you need to write the query to manually change the is_internal flag to true in the database.

And then as discussed in the previous round, you need to implement the logic and UI changes to allow internal users to impersonate other users.

If you need any help or have any questions, feel free to reach out to me at 314-562-8039 or naren@wolfia.com. Good luck!

## FAQ

### Making changes to the database

We are using alembic to manage database migrations. To make changes to the database, you will need to create a new migration file. You can do this by running the following command from the backend directory:

```sh
docker compose exec backend alembic revision -m "message about the migration"
```

This will create a new migration file in the `alembic/versions` directory. You can then make the necessary changes to the database schema in the `upgrade` function. Also make sure to add the necessary changes to the `downgrade` function to rollback the changes. Once you are done, you can run the migration by running the following command from the backend directory:

```sh
docker compose exec backend alembic upgrade head
```

If you want to downgrade the migration, you can run the following command:

```sh
docker compose exec backend alembic downgrade -1
```

This will rollback the last migration. You can also specify the number of migrations to rollback by changing the number after the `-` sign.

## Common Issues and Troubleshooting

### Issue: Docker containers won't start

- Ensure Docker and Docker Compose are installed and running. Download and install Docker Desktop from [here](https://www.docker.com/products/docker-desktop).
- Check that all environment variables are correctly set in the local.env file.

### Issue: Database migrations are not running

- Ensure the database is running and accessible. You can verify this using `docker compose logs db`.
- Ensure the database schema is up-to-date by running `alembic upgrade head`.
- If the issue persists, try restarting the database container using `docker compose restart db`.

### Issue: Frontend dependencies are not installing

- Ensure you are running the frontend container using `docker compose up --build`.
- Install the dependencies manually by running `docker compose exec frontend npm install`.