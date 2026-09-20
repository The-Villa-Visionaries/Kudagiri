# Kudagiri
Imagine there is an island that serves as a resort and offers accommodation for tourists. We are planning to open a theme park on a separate island nearby. We are making an online booking system for the resort island, theme park island, and the ferry service that operates between the two islands!

# Contributors
Aishath Livaa Ahmed <br>
Ahmed Dhaavoodhu Ali <br>
Aishath Nausheen Waseem <br>
Ibrahim Jinaah

## Technology Stack
| Component | Technology |
|---|---|
| Frontend | React, TypeScript, Vite |
| Styling | Tailwind CSS |
| Backend | Python, FastAPI |
| Database | SQLite |
| API Server | Uvicorn |

## Setup Instructions
Install the following before setting up the project:

Python 3.11 or newer <br>
Node.js and npm <br>
Git

**1. Clone the repository** <br>
```git clone https://github.com/livv88/Kudagiri``` <br>
```cd Kudagiri``` <br>

**2. Set up backend** <br>
Create and activate a Python virtual environment from the project root. <br>

Windows PowerShell: <br>
```python -m venv .venv``` <br>
```.\.venv\Scripts\Activate.ps1``` <br>

macOS/Linux: <br>
```python3 -m venv .venv``` <br>
```source .venv/bin/activate``` <br>

Install the Python dependencies: <br>
```python -m pip install -r requirements.txt``` <br>

**3. Set up frontend** <br>
Open a second terminal and move into the frontend directory: 

```cd frontend``` <br>
```npm install``` <br>

## Initializing Database
The active FastAPI application automatically creates the SQLite tables it requires when "backend/main.py" starts. No separate database server is required.

Start the backend from the project root so that the SQLite database is created/used in the expected location:

```cd backend``` <br>
```uvicorn backend.main:app --reload```

The API will be available at:

```http://localhost:8000```

FastAPI's interactive API documentation is available at:

```http://localhost:8000/docs```

## Running Backend and Frontend
From the project root, with the virtual environment activated:

```uvicorn backend.main:app --reload```

Keep this terminal running while using the frontend.

In a second terminal:

```cd frontend```
```npm run dev```

Vite will display the local development address in the terminal, normally:

```http://localhost:5173```

Open that address in a web browser.

## Default Test Users
| Username | Role | Email | Password |
|---|---|---|---|
| NighRaven | Admin | nightraven@example.com | 1 |
| Livv | User |livv@example.com | 2 |
| Naushyn | User |naushyn@example.com | 3 |
| Jinaah | User | jinaah@example.com | 4 |

## Main Features
User registration and login <br>
Role-based access for visitors, staff and administrators <br>
Theme park island map <br>
Booking hotels, ferry rides, theme park activties and beach events <br>
Advertisement banners and promotion codes <br>
Session management <br>
Activity logging in the backend <br>
Responsive React-based user interface <br>
SQLite database for local persistence <br>

## Security Notice
SQLite database files are intended for local development. They should not be relied on as a shared production database. <br>
The application is intended for local development/demo use and does not currently provide production deployment configuration. <br>

The credentials listed above are development-only seed values from the repository and must not be reused for real accounts.