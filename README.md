# DevTrack — Engineering Issue Tracker API

## Overview

DevTrack is a Django-based backend API for tracking engineering issues. It allows users to register reporters, create issues, assign priorities, and track issue statuses.

The project demonstrates Object-Oriented Programming (OOP), API development, input validation, and JSON file-based data storage.

## Technologies Used

- Python
- Django
- JSON
- Postman
- Object-Oriented Programming (OOP)

## Features

- Create and retrieve reporters.
- Create and retrieve engineering issues.
- Filter issues by ID and status.
- Validate issue titles, priorities, and statuses.
- Check that an issue's reporter exists.
- Prevent duplicate IDs.
- Generate different descriptions for critical and low-priority issues.
- Return appropriate HTTP status codes for successful requests and errors.

## Project Structure

```text
DevTrack/
├── devtrack/
│   ├── settings.py
│   └── urls.py
├── issues/
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── reporters.json
├── issues.json
├── manage.py
├── .gitignore
└── README.md
```

## Object-Oriented Programming Concepts

- **Abstraction:** `BaseEntity` defines a common validation interface.
- **Inheritance:** `Reporter` and `Issue` inherit from `BaseEntity`.
- **Method overriding:** `CriticalIssue` and `LowPriorityIssue` override the `describe()` method.
- **Encapsulation of behavior:** Classes keep related data and validation or description methods together.
- **Polymorphism:** Different issue subclasses provide different descriptions through the same `describe()` method.

## API Endpoints

Base URL: `http://127.0.0.1:8000`

### Reporters

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/reporters/` | Create a reporter |
| GET | `/api/reporters/` | Retrieve all reporters |
| GET | `/api/reporters/?id=1` | Retrieve a reporter by ID |

Example reporter request:

```json
{
  "id": 1,
  "name": "Khushi Tyagi",
  "email": "khushi@example.com",
  "team": "backend"
}
```

### Issues

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/issues/` | Create an issue |
| GET | `/api/issues/` | Retrieve all issues |
| GET | `/api/issues/?id=1` | Retrieve an issue by ID |
| GET | `/api/issues/?status=open` | Filter issues by status |

Example issue request:

```json
{
  "id": 1,
  "title": "Login button not working on mobile",
  "description": "The login button does not respond on mobile devices.",
  "status": "open",
  "priority": "critical",
  "reporter_id": 1
}
```

Allowed statuses:

- `open`
- `in_progress`
- `resolved`
- `closed`

Allowed priorities:

- `low`
- `medium`
- `high`
- `critical`

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/khushityaagi/DevTrack.git
cd DevTrack
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment on Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Django

```bash
python -m pip install django
```

### 5. Initialize the database

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

The API server will be available at `http://127.0.0.1:8000`.

## Testing

The endpoints were tested using Postman, including:

- Successful reporter creation and retrieval.
- Successful issue creation and retrieval.
- Filtering issues by status.
- Validation of empty issue titles.
- Handling of nonexistent issue IDs.

Screenshots of the Postman tests can be added to this README after they are saved in the repository.

## Data Storage

This project uses `reporters.json` and `issues.json` for persistent data storage. The Django SQLite database file is not used as the primary store for these API records.

## Future Improvements

- Replace JSON file storage with Django models and a relational database.
- Add automated unit and integration tests.
- Add authentication and permissions.
- Improve API structure using Django REST Framework.
- Add pagination and more advanced filtering.

## Author

Khushi Tyagi
