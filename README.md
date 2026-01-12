# django-forum

A reddit-like forum where users can post, comment, get authenticated, place adverts.

## Deploy to Render (via GitHub)

This repo includes a Render Blueprint file: `render.yaml`.

1. Push this repository to GitHub.
2. On Render, click **New +** → **Blueprint** and select your GitHub repo.
3. Render will create:
   - a web service (`django-forum`)
   - a managed Postgres database (`django-forum-db`)

The web service is configured to:
- **Build:** install dependencies and run `collectstatic`
- **Start:** run migrations and start Gunicorn

## Environment variables

Set these on Render (the Blueprint sets most of them automatically):
- `SECRET_KEY`
- `DEBUG=0`
- `ALLOWED_HOSTS=.onrender.com`
- `DATABASE_URL` (from the Render Postgres database)

Optional (only needed for advert payments):
- `STRIPE_PUBLISHABLE_KEY`
- `STRIPE_SECRET_KEY`

## Migrating existing data from SQLite to Postgres

If you want to keep the data currently in `db.sqlite3`:

1) Dump your SQLite data (PowerShell):

    python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission |
      Out-File -Encoding utf8 data.json

2) Point Django at Postgres by setting `DATABASE_URL`, then run:

    python manage.py migrate
    python manage.py loaddata data.json
