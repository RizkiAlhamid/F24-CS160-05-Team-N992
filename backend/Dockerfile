# Use the official Python image as the base image
FROM python:3.12-slim

# Set environment variables
ENV POETRY_VERSION=1.8.3 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && apt-get clean

# Install Poetry using the official method
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry  # Create a symlink for Poetry

# Set the working directory
WORKDIR /app

# Copy only the necessary files for Poetry to install dependencies
COPY poetry.lock pyproject.toml /app/

# Install dependencies with Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app

# Expose the port FastAPI will run on
EXPOSE 8080

# Start FastAPI server
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
