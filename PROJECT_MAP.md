# TaskFlow AI - Project Map

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Backend | Flask | 3.1.3 |
| ORM | SQLAlchemy | 2.0.51 |
| Auth | Flask-Login | 0.6.3 |
| AI | OpenAI SDK | 2.45.0 |
| Frontend | React | 19.1.0 |
| Routing | React Router | 7.6.1 |
| Styling | Tailwind CSS | 4.1.7 |
| Build | Vite | 6.4.3 |

## Project Structure

```
taskflow/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # App factory + blueprint registration
│   │   ├── config.py            # Dev/Prod/Testing configs
│   │   ├── extensions.py        # db, migrate, login_manager, CORS
│   │   ├── auth/                # Auth domain (4 files)
│   │   │   ├── __init__.py
│   │   │   ├── models.py        # User model (UUID PK, Google OAuth)
│   │   │   ├── routes.py        # register, login, google, me, logout
│   │   │   └── services.py      # create_user, authenticate_email, google
│   │   ├── tasks/               # Tasks domain (4 files)
│   │   │   ├── __init__.py
│   │   │   ├── models.py        # Task, Project, TaskStatus, TaskPriority
│   │   │   ├── routes.py        # CRUD endpoints for tasks & projects
│   │   │   └── services.py      # Business logic for tasks & projects
│   │   ├── ai/                  # AI domain (4 files)
│   │   │   ├── __init__.py
│   │   │   ├── models.py        # Conversation, Message
│   │   │   ├── routes.py        # SSE chat, models list, playground
│   │   │   └── services.py      # Stream chat, model list, playground
│   │   └── shared/              # Shared utilities
│   │       ├── __init__.py
│   │       ├── responses.py     # success_response, error_response
│   │       ├── errors.py        # Error handlers
│   │       └── logging_config.py
│   ├── tests/
│   │   ├── conftest.py          # Fixtures: app, client, auth_client
│   │   ├── test_auth.py         # 12 auth tests (incl. Google OAuth)
│   │   ├── test_tasks.py        # 10 task tests
│   │   └── test_ai.py           # 5 AI tests
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── wsgi.py
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── main.jsx             # React entry point
│   │   ├── App.jsx              # Router + protected routes
│   │   ├── index.css            # Tailwind import
│   │   ├── context/
│   │   │   └── AuthContext.jsx  # Auth state + login/register/googleLogin/logout
│   │   ├── lib/
│   │   │   └── api.js           # Axios instance + interceptors
│   │   └── pages/
│   │       ├── Landing.jsx      # Marketing landing page
│   │       ├── Login.jsx        # Email/password + Google OAuth
│   │       ├── Register.jsx     # Registration + Google OAuth
│   │       ├── Dashboard.jsx    # Stats overview + recent tasks
│   │       ├── Tasks.jsx        # Full CRUD task management
│   │       └── AIPlayground.jsx # Chat + model playground (SSE)
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── vite.config.js
│   └── package.json
├── docker-compose.yml
├── Makefile
└── .env
```

## API Endpoints

### Auth (`/api/auth`)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /register | No | Register with email/password |
| POST | /login | No | Login with email/password |
| POST | /google | No | Login with Google OAuth token |
| GET | /me | Yes | Get current user |
| POST | /logout | Yes | Logout |

### Tasks (`/api`)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /tasks | Yes | List tasks (filter: ?status=) |
| POST | /tasks | Yes | Create task |
| GET | /tasks/:id | Yes | Get single task |
| PUT | /tasks/:id | Yes | Update task |
| DELETE | /tasks/:id | Yes | Delete task |
| GET | /projects | Yes | List projects |
| POST | /projects | Yes | Create project |
| GET | /projects/:id | Yes | Get project with tasks |
| PUT | /projects/:id | Yes | Update project |
| DELETE | /projects/:id | Yes | Delete project |

### AI (`/api/ai`)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /models | Yes | List available AI models |
| POST | /chat | Yes | SSE stream chat about tasks |
| GET | /conversations | Yes | List conversations |
| POST | /playground | Yes | SSE stream custom prompt |

## Quick Start

```bash
# Development
make install
make dev-backend    # Terminal 1: Flask on :5000
make dev-frontend   # Terminal 2: Vite on :5173

# Production (Docker)
cp .env.example .env  # Add your OPENAI_API_KEY
make docker-up

# Tests
make test
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| SECRET_KEY | Yes | dev-secret-change-me | Flask secret key |
| DATABASE_URL | No | sqlite:///taskflow.db | Database URI |
| OPENAI_API_KEY | Yes | - | OpenAI API key |
| GOOGLE_CLIENT_ID | No | - | Google OAuth client ID (backend) |
| GOOGLE_CLIENT_SECRET | No | - | Google OAuth client secret (backend) |
| VITE_GOOGLE_CLIENT_ID | No | - | Google OAuth client ID (frontend, from Google Cloud Console) |
