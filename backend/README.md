# FastAPI Project

This is a FastAPI project structure using Poetry for dependency management. Follow the instructions below to set up the project, manage dependencies, and run the application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setting Up Poetry](#setting-up-poetry)
- [Adding Dependencies](#adding-dependencies)
- [Removing Dependencies](#removing-dependencies)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)

## Prerequisites

- Python 3.12 or higher
- Poetry installed on your system

You can install Poetry by following the instructions at [Poetry's official installation guide](https://python-poetry.org/docs/#installation).

## Installation

1. Clone the repository:

```bash
git clone https://github.com/RizkiAlhamid/F24-CS160-05-Team-N992.git
cd F24-CS160-05-Team-N992/backend
```

2. Install dependencies using Poetry:

```bash
poetry install
```

## Setting Up Poetry

To activate the virtual environment created by Poetry, run the following command:

```bash
poetry shell
```

## Adding Dependencies

To add a new dependency to the project, use the following command:

```bash
poetry add <package-name>
```

## Removing Dependencies

To remove a dependency from the project, use the following command:

```bash
poetry remove <package-name>
```

## Running the Application

To run the FastAPI application, use the following command:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

or run the run_dev.sh script

```bass
./run_dev.sh
```

The application will be accessible at `http://localhost:8080`.

## Running Tests

To run the tests for the FastAPI application, use the following command:

```bash
pytest
```

