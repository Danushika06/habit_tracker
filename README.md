# Habit Tracker

**A small full-stack habit tracker: a Django REST API on PostgreSQL and a React + Tailwind front end where you add habits, tick them off each day, and see streaks, completion rates and a seven-day strip.**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white) ![Django REST Framework](https://img.shields.io/badge/DRF-A30000?style=flat&logo=django&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white) ![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB) ![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white) ![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-06B6D4?style=flat&logo=tailwindcss&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)

## Overview

Habits stick better when you can see a streak. This project is a minimal tracker for that: create a habit with a name and a category, check it off for today, and watch the current streak and completion percentage update.

It is deliberately small. There are no user accounts, so the API is open to anyone who can reach it (the settings say so explicitly), and the whole thing is one Django app (`habits`) plus one React page. I built it as a compact end-to-end exercise in wiring a React front end to a Django REST backend on PostgreSQL.

Status: the core loop works against a local backend. The front end currently has the API address hard-coded to a local development server, and the repo has no tests (the `tests.py` file is the generated stub). The repo is also said to have a GitHub Actions workflow, but it was not part of the files I worked from, so I have not described it here.

## Key Features

- **Habits with categories** - `Habit` has a name, a category and a creation timestamp; the UI has an add form and a category filter built from the categories that exist.
- **Daily check-off** - ticking the checkbox on a card calls `POST /api/habits/<id>/toggle/`, which creates or deletes a `HabitLog` for the date and returns `{"checked": true|false}`. A database constraint (`unique_habit_completed_date`) stops a habit being logged twice on one day.
- **Streaks** - `Habit.current_streak()` counts consecutive logged days going back from today. If today is not logged, the streak reads 0.
- **Completion rate** - `Habit.completion_rate()` is logged days divided by the days since the habit was created, as a percentage rounded to one decimal.
- **Seven-day strip** - each card shows the last seven days as small squares, filled green when a log exists (`getLastNDays` in `frontend/src/utils/date.js`).
- **Delete** - `DELETE /api/habits/<id>/` removes a habit and, by cascade, its logs.
- **Single-deployment option** - settings configure WhiteNoise to serve the built React app from `frontend/dist` through Django, so one process can serve both.

## How It Works

**Backend.** `backend/config/` holds the Django project. `backend/habits/` holds the models, serializers, views and URLs, mounted under `/api/` in `config/urls.py`. `HabitSerializer` returns each habit with its nested logs plus the computed `current_streak` and `completion_rate`, so the front end gets everything for a card from one list call. DRF is set to use no authentication classes and `AllowAny` permissions.

**Configuration.** `config/settings.py` reads everything from environment variables via `python-dotenv`: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` (defaults to false), `DJANGO_ALLOWED_HOSTS` (comma-separated), and `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` for PostgreSQL. CORS allows `http://localhost:5173`, the Vite dev server.

**Frontend.** `frontend/src/App.jsx` fetches the habit list on load, posts new habits, and filters by category. Each habit renders as a `HabitCard` that calls the toggle and delete endpoints and then asks `App` to refetch. API calls use plain `fetch`, and the base URL is `API_URL` in `frontend/src/config.js`.

## Tech Stack

- **Backend:** Python, Django 6.1, Django REST Framework 3.18.0, django-cors-headers, WhiteNoise, psycopg 3
- **Database:** PostgreSQL
- **Frontend:** React 19, Vite 8, Tailwind CSS 4 (through `@tailwindcss/vite`), oxlint
- **Config:** python-dotenv

## Getting Started

### Prerequisites
- Python 3 and `pip`
- Node.js and `npm`
- A running PostgreSQL database

### Installation
```bash
git clone https://github.com/Danushika06/habit_tracker.git
cd habit_tracker

# backend
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Use `backend/requirements.txt`; the copy in the repo root is missing `whitenoise`, which the settings need.

Create `backend/.env` with the variables listed under Configuration (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`). `.env` is gitignored.

```bash
# frontend (from the repo root)
cd frontend
npm install
```

### Running
```bash
# terminal 1: API on http://127.0.0.1:8000
cd backend
python manage.py migrate
python manage.py runserver

# terminal 2: UI on http://localhost:5173
cd frontend
npm run dev
```

Other front-end scripts from `package.json`: `npm run build`, `npm run lint` (oxlint) and `npm run preview`.

To serve the built app through Django instead, run `npm run build` in `frontend/` so that `frontend/dist` exists; WhiteNoise is set to serve it from there. Note that `API_URL` is still the local address, so change it first if the API is not on `127.0.0.1:8000`.

## Usage

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/api/habits/` | List habits with logs, current streak and completion rate |
| POST | `/api/habits/` | Create a habit; JSON body with `name` and `category` |
| DELETE | `/api/habits/<id>/` | Delete a habit and its logs |
| POST | `/api/habits/<id>/toggle/` | Toggle a log for today, or for a `date` in the body; returns `{"checked": bool}` |

In the UI: type a habit name and category and press Add, tick a card to log today (untick to undo), pick a category in the dropdown to filter, and use Delete to remove a habit.

Things to know: the API has no authentication, so do not expose it publicly as is. The streak is calculated in the server's date (UTC per `TIME_ZONE`), while the front end decides "today" from the browser's local date, so the two can disagree around midnight.

## Project Structure

```
habit_tracker/
├── backend/
│   ├── manage.py
│   ├── requirements.txt        # use this one
│   ├── config/                 # settings.py (env-driven), urls.py, wsgi/asgi
│   └── habits/
│       ├── models.py           # Habit (streak, completion rate), HabitLog
│       ├── serializers.py
│       ├── views.py            # list/create, delete, toggle
│       ├── urls.py
│       └── migrations/         # 0001_initial, 0002_habitlog
├── frontend/
│   ├── package.json
│   ├── vite.config.js          # React + Tailwind plugins
│   └── src/
│       ├── App.jsx             # list, add form, category filter
│       ├── config.js           # API_URL
│       ├── components/HabitCard.jsx
│       └── utils/date.js
└── requirements.txt            # older copy, lacks whitenoise
```

---

## Contact

<table>
  <tr><td><b>GitHub:</b> <a href="https://github.com/Danushika06">Danushika06</a></td><td><b>LinkedIn:</b> <a href="https://www.linkedin.com/in/danushika-n-323b4628b/">danushika-n</a></td></tr>
  <tr><td colspan="2" align="center"><b>Email:</b> <a href="mailto:danushikanagarajan@gmail.com">danushikanagarajan@gmail.com</a></td></tr>
</table>

Built by **Danushika N**
