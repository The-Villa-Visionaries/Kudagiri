# Kudagiri backend

## Progress and scope

The backend was an empty scaffold at `56e40c7` on `Co-Developement`.
Work is divided into three separate commits on that branch:

1. **Hotels and rooms:** FastAPI startup, the master API router, SQLite models,
   catalogue queries, validation, and tests. Completed in Part 1 (`b3a7014`).
2. **Authentication:** `api/auth.py`, user model/schema, password hashing and
   token helpers, signup/login service, and authentication tests. Completed in Part 2 (`bcd266a`).
3. **Bookings and tickets:** `api/bookings.py`, booking/ticket models and schemas,
   authenticated reservations, date/guest validation, pricing, availability and
   double-booking protection, cancellation, staff ticket validation, and tests.
   Implemented in Part 3 and registered in `api/router.py`.

Before Part 2, teammate commit `1b26cd2` ("Verified", September 13) was reviewed
and fast-forwarded into the working branch. Its backend edits are preserved.

Before Part 3, the branch was synced through `e3ba3a9` (September 18, staff
theme-park page). Incoming changes were frontend-only. The supporting database,
models, schemas, and services are implemented, and completed task placeholders
have been removed. The frontend still needs to be connected to these APIs.

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
adds the `users` table without changing existing hotel or room tables. Part 3
only adds new tables (`bookings`, `room_nights`, `ticket_sessions`, `tickets`,
and `ticket_staff`); existing users, rooms, and hotel data are preserved.

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
If no ticket sessions exist, the same command also adds a demo ferry and a demo
theme-park session for tomorrow (Maldives time). Existing sessions are untouched.
These are fictional schedules, capacities, and prices for development. Real
inventory must be entered by a trusted database operator; no public catalogue
editing API is provided. The seed does not replenish expired sessions.

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
- `check_in` and `check_out`: optional paired dates added in Part 3; return only
  rooms free for the entire stay. Checkout is exclusive, so back-to-back stays
  are allowed. All other filters and pagination still apply.

Example: `/api/rooms?category=family&guests=4&max_price=700&sort=price_asc`.
Prices are JSON decimal strings, for example `"650.00"`, to preserve cents.
`200` means success (including an empty list), `404` means the requested hotel
or room does not exist, and `422` means invalid parameters. Error bodies use
FastAPI's `detail` field. Without both dates, results describe the room catalogue,
not availability. A search result does not hold a room; the reservation request
checks availability when committing.

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
The reusable `get_current_user` dependency in `api/auth.py` identifies booking
owners; clients must not choose another user's ID themselves.

- `409`: email already registered, including simultaneous duplicate signups.
- `401`: incorrect credentials, missing/invalid/expired token, or deleted account.
- `422`: invalid request data. Validation errors omit submitted values to avoid
  exposing passwords. Successful account and token responses use `Cache-Control: no-store`.

The frontend has not been connected to these routes. Part 2 does not add email
verification, password reset, refresh tokens, or server-side logout/revocation.
Clients can discard their token to sign out; issued tokens remain valid until
expiry unless the signing key changes or the account is removed. Before public
deployment, add login/signup rate limiting and serve authentication over HTTPS.

## Part 3 API

All booking and ticket operations require the bearer token from Part 2, except
the public ticket-session catalogue. Users only see their own records; another
user's record returns `404`. Lists return `items`, `total`, `skip`, and `limit`.
The default page size is 20, with a maximum of 100. Booking/ticket lists also
accept `status=confirmed` or `status=cancelled` and include both by default.

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/api/bookings` | Reserve a room; returns `201` |
| GET | `/api/bookings` | List my room reservations |
| GET | `/api/bookings/{id}` | View my reservation |
| POST | `/api/bookings/{id}/cancel` | Cancel my future reservation |
| GET | `/api/ticket-sessions` | Public ferry/theme-park sessions that have not ended |
| GET | `/api/ticket-sessions/{id}` | Session details and remaining capacity |
| POST | `/api/tickets` | Reserve ticket entries; returns `201` and a unique code |
| GET | `/api/tickets` | List my tickets |
| GET | `/api/tickets/{id}` | View my ticket, price, session, and usage |
| POST | `/api/tickets/{id}/cancel` | Cancel my unused future ticket |
| GET | `/api/tickets/staff-permissions` | My allowed ticket kinds (empty for ordinary users) |
| POST | `/api/tickets/validate` | Staff: check a code for a selected session |
| POST | `/api/tickets/redeem` | Staff: consume one or more ticket entries |

Room reservation request (replace the dates with future dates):

```json
{"room_id": 1, "check_in": "2030-01-11", "check_out": "2030-01-14", "guests": 2}
```

Check-in cannot be in the past, checkout must follow check-in, and a stay is
limited to 365 nights. The guest count must fit the room. Each room record is
one independently bookable unit, not a room category with multiple units.
Dates use Maldives time (UTC+5), independent of the computer/server timezone.

Ticket reservation request:

```json
{"session_id": 1, "quantity": 2}
```

The catalogue accepts `kind=ferry` or `kind=theme_park`, and an optional
`session_date=YYYY-MM-DD` filter in Maldives time. Timestamps include UTC offsets.
Purchases must occur before `starts_at`; quantity must be an integer from 1 to
100 and fit the remaining capacity. A group ticket code represents `quantity`
entries in that single session. Ferry tickets are for one scheduled journey;
reserve the return journey separately when available.

Room totals are the stored nightly price multiplied by nights. Ticket totals
are the stored session price multiplied by quantity. Decimal prices and currency
are saved with each reservation, so later catalogue price changes do not alter
the agreed total. Clients cannot supply prices, ownership, or status fields.
These are reservations: no payment is collected or represented as paid, and
the frontend's placeholder taxes/discounts/promo codes are not applied.

Current cancellation defaults (pending team business-rule confirmation):

- Rooms: before the check-in date begins in Maldives time.
- Tickets: before the session starts, and only if no entries have been redeemed.
- Cancellation retains the record, releases availability, and can be repeated
  safely without releasing the same inventory twice. There is no refund operation.

Room-night uniqueness is enforced by a database primary key. Reserving multiple
nights is one transaction: if any night conflicts, the entire reservation is
rolled back. Ticket capacity uses a conditional SQL update and a database check
constraint. Redemption uses another conditional update, preventing simultaneous
requests from redeeming more entries than purchased. These follow SQLAlchemy's
[constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html) and
[update](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html) mechanisms.

Successful reads/cancellations return `200`, creates `201`, missing authentication
`401`, missing staff permission `403`, missing/inaccessible records `404`,
unavailable inventory or invalid state `409`, and invalid input `422`.
Creation requests are not idempotent: do not automatically retry ticket purchases
after an uncertain network response; first check the user's existing tickets.

### Staff ticket checks

Changing `?role=Admin` in the frontend grants no API permission. A trusted local
database operator must assign permission to an existing account. No account is
automatically promoted, and signup does not accept roles. Start the API once to
create its tables, then run from `backend` only for an approved staff account:

```powershell
.\.venv\Scripts\python.exe -m app.manage_staff --email staff@example.com --kind theme_park
# Revoke the same permission:
.\.venv\Scripts\python.exe -m app.manage_staff --email staff@example.com --kind theme_park --revoke
```

Ferry permission is separate (`--kind ferry`). Permission is checked from the
database on every request, so revocation also affects already-issued tokens.
The frontend can call `/api/tickets/staff-permissions` to decide which staff
controls to show; API authorization still runs regardless of what is displayed.

Validation body: `{"ticket_code": "<code from reservation>", "session_id": 1}`.
Redemption uses the same body plus `"quantity": 1`. Staff can validate/redeem
only their permitted kind and the exact selected session. Codes must be active,
have unused entries, and belong to the current Maldives calendar day; they
expire at `ends_at`. Same-day early boarding/admission is allowed by this default.
Repeated scans consume additional entries until none remain, so the UI should
require an explicit quantity and prevent accidental double submission.

The ticket code is generated by the backend when a customer reserves. Printing
that code is frontend work. Creating tickets on behalf of other users, payments,
catalogue editing, and team-specific pricing/cancellation rules are outside this
implementation. Tests use temporary databases and never grant staff privileges
to a real local account.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Tests use temporary SQLite databases, never the local catalogue. They exercise
responses, filters, pagination, error codes, CORS, persistence, foreign keys,
and repeatable demo seeding. Authentication tests cover signup/login, concurrent
duplicate accounts, password secrecy, token validation, account persistence,
CORS, and missing/invalid signing configuration.
Part 3 tests cover dates, calculated prices, ownership, persistence, availability,
concurrent reservations, capacity limits, cancellation, staff permissions, and
concurrent ticket redemption/cancellation.

## Before future changes

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
