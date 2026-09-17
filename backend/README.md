# Kudagiri backend

## Progress and scope

The backend was an empty scaffold at `56e40c7` on `Co-Developement`.
Work is divided into three separate commits on that branch:

1. **Hotels and rooms:** FastAPI startup, the master API router, SQLite models,
   catalogue queries, validation, and tests. Completed in Part 1 (`b3a7014`).
2. **Authentication:** `api/auth.py`, user model/schema, password hashing and
   token helpers, signup/login service, and authentication tests. Implemented in Part 2.
3. **Bookings and tickets:** `api/bookings.py`, booking/ticket models and schemas,
   authenticated reservations, date/guest validation, pricing, availability and
   double-booking protection, plus tests. Pending; register its router in `api/router.py`.

Before Part 2, teammate commit `1b26cd2` ("Verified", September 13) was reviewed
and fast-forwarded into the working branch. Its backend edits are preserved.

The API task notes remain until all three parts are finished. The database,
models, schemas, and service files in Part 1 support the hotel routes; those
folders were also empty. The existing frontend still uses hardcoded data and
needs to be connected to the API by the frontend team.

## Run locally

Use Python 3.10 or later. From this `backend` directory, in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
# Set SECRET_KEY in .env before starting (see below).
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Copy `.env.example` only when you do not already have a `.env` file. The default
database is `backend/kudagiri.db`; tables are created at startup. `.env`, the
database, dependencies, and logs are ignored by Git. Changing an existing table
will need a migration in future; startup only creates missing tables. Part 2
adds the `users` table without changing existing hotel or room tables.

Generate a local signing key, then put it in `SECRET_KEY` in your ignored `.env`:

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(48))"
```

Keep the key private and stable between restarts. There is no built-in fallback
key: startup fails if it is missing or shorter than 32 non-padding characters.
Changing the key invalidates existing tokens. `ACCESS_TOKEN_EXPIRE_MINUTES`
defaults to 30 and accepts 1 to 1440 minutes. Tests inject their own test-only key.

- API documentation: <http://127.0.0.1:8000/docs>
- Health check: <http://127.0.0.1:8000/health>
- Frontend: run `npm ci`, then `npm run dev` from `frontend`.

The catalogue starts empty. For optional local demonstration data:

```powershell
.\.venv\Scripts\python.exe -m app.seed
```

This adds one **demo** hotel and four sample rooms only when no hotel exists.
It does not run automatically, overwrite existing hotels, or represent real
inventory/pricing. Room prices currently use USD, matching the frontend mockup.
The seed data has no room images; `image_url` may be null.

## Part 1 API

All catalogue routes are public reads. Management/write routes and authentication
are outside Part 1. The health route is a process liveness check.

| Method | Path | Result |
| --- | --- | --- |
| GET | `/health` | `{"status":"ok"}` |
| GET | `/api/hotels` | Paginated hotels |
| GET | `/api/hotels/{hotel_id}` | One hotel |
| GET | `/api/hotels/{hotel_id}/rooms` | Rooms belonging to a hotel |
| GET | `/api/rooms` | Rooms across hotels |
| GET | `/api/rooms/{room_id}` | One room |

Lists return `items`, `total` (before pagination), `skip`, and `limit`.
Both lists accept `skip` (default 0) and `limit` (default 20, maximum 100).
Room lists also accept:

- `q`: case-insensitive room name/description search, 1 to 100 characters.
- `category`: `beachfront`, `ocean_suite`, `garden`, or `family`.
- `guests`: minimum room capacity, at least 1.
- `max_price`: inclusive nightly USD price ceiling, nonnegative, up to 2 decimal places.
- `sort`: `name` (default), `price_asc`, or `price_desc`.

Example: `/api/rooms?category=family&guests=4&max_price=700&sort=price_asc`.
Prices are JSON decimal strings, for example `"650.00"`, to preserve cents.
`200` means success (including an empty list), `404` means the requested hotel
or room does not exist, and `422` means invalid parameters. Error bodies use
FastAPI's `detail` field. Capacity filtering is not date-based availability;
check-in/check-out and reservations belong to Part 3.

Request flow: `main.py` mounts `api/router.py`; `api/hotels.py` validates the
request and calls `services/serviceHotels.py`; that service queries SQLAlchemy
models through a database session; `schemas/schemaHotel.py` defines the JSON
response. This follows the [FastAPI router guide](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
and [SQLAlchemy ORM guide](https://docs.sqlalchemy.org/en/20/orm/quickstart.html).

## Part 2 API

| Method | Path | Result |
| --- | --- | --- |
| POST | `/api/auth/signup` | `201`: account ID, full name, and normalized email |
| POST | `/api/auth/login` | `200`: access token, `token_type`, and `expires_in` (seconds) |
| GET | `/api/auth/me` | `200`: the account identified by a valid bearer token |

Signup accepts a JSON body:

```json
{
  "full_name": "Example Guest",
  "email": "guest@example.com",
  "password": "choose-your-own-password"
}
```

Login accepts just `email` and `password` as JSON. Emails are validated and
normalized to lowercase, so different casing cannot create duplicate accounts.
Full names must contain 1 to 100 characters after trimming. Signup passwords
must contain 8 to 128 characters and cannot be all whitespace; their original
spaces and Unicode characters are preserved. Unknown fields are rejected.

Passwords are stored as salted Argon2 hashes and never returned. Part 2 replaces
the scaffold's unused Passlib/python-jose entries with pwdlib and PyJWT, following
the [current FastAPI authentication guide](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/).
Tokens use HS256 with an expiry, user ID, issuer, audience, and access-token type.

Send `Authorization: Bearer <access_token>` to `/api/auth/me`. In Swagger, execute
signup and login first, then use **Authorize** and paste only the access token.
The reusable `get_current_user` dependency in `api/auth.py` will identify booking
owners in Part 3; clients must not choose another user's ID themselves.

- `409`: email already registered, including simultaneous duplicate signups.
- `401`: incorrect credentials, missing/invalid/expired token, or deleted account.
- `422`: invalid request data. Validation errors omit submitted values to avoid
  exposing passwords. Successful account and token responses use `Cache-Control: no-store`.

The frontend has not been connected to these routes. Part 2 does not add email
verification, password reset, refresh tokens, or server-side logout/revocation.
Clients can discard their token to sign out; issued tokens remain valid until
expiry unless the signing key changes or the account is removed. Before public
deployment, add login/signup rate limiting and serve authentication over HTTPS.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Tests use temporary SQLite databases, never the local catalogue. They exercise
responses, filters, pagination, error codes, CORS, persistence, foreign keys,
and repeatable demo seeding. Authentication tests cover signup/login, concurrent
duplicate accounts, password secrecy, token validation, account persistence,
CORS, and missing/invalid signing configuration.

## Before Parts 2 and 3

Work from the Git clone, not the original downloaded ZIP. From the repository root:

```powershell
git status --short --branch
git switch Co-Developement
git fetch origin
git log --oneline HEAD..origin/Co-Developement -- backend
git diff HEAD...origin/Co-Developement -- backend
git merge --ff-only origin/Co-Developement
```

Check for local changes before switching or merging. Review incoming backend
changes and adjust the next part to reuse teammates' work. If history diverges,
inspect and reconcile it without force-pushing or discarding anyone's work.
Rerun backend tests before and after the next part. Fetch again before pushing
because a teammate may have committed while work was underway.

Commit each completed part on the actual day it is worked on, using the configured
Git identity and a message describing the change. Stage only reviewed backend
files and push explicitly to `Co-Developement`. Do not push to `main`.
