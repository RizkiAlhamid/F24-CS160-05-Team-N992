# FastAPI Project

This is a FastAPI project structure using Poetry for dependency management. Follow the instructions below to set up the project, manage dependencies, and run the application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setting Up Poetry](#setting-up-poetry)
- [Adding Dependencies](#adding-dependencies)
- [Removing Dependencies](#removing-dependencies)
- [Running the Application](#running-the-application)

## Prerequisites

- Python 3.12 or higher
- Poetry installed on your system
- MongoDB URI in .env file (MONGO_URI)

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

Make sure you have .env file in the root directory of the project.
To run the FastAPI application, use the run_dev.sh script:

```bass
./run_dev.sh
```

The application will be accessible at `http://localhost:8080`.
