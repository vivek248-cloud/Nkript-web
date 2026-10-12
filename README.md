# Nkript Portfolio & Quotation Website (Django)

A runnable starter project for a freelancing agency website with:
- Dynamic portfolio projects and multiple screenshots
- Website categories and packages with min/max prices
- Admin-managed tier features and priced add-ons
- Client quotation request form
- Database-stored quote and selected-feature snapshots
- Email notification to the client and admin
- Django Admin management
- Media upload support

## Requirements
- Python 3.10+
- Django 5.2
- Pillow

## Install on Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

The initial migration is included at `core/migrations/0001_initial.py`. If you change models, run:
```powershell
python manage.py makemigrations
python manage.py migrate
```

## Configure email
By default, development email uses Django's console backend: messages print in the terminal.
For SMTP, set environment variables before running the server:
```powershell
$env:EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
$env:EMAIL_HOST="smtp.gmail.com"
$env:EMAIL_PORT="587"
$env:EMAIL_USE_TLS="True"
$env:EMAIL_HOST_USER="your-account@gmail.com"
$env:EMAIL_HOST_PASSWORD="your-google-app-password"
$env:DEFAULT_FROM_EMAIL="your-account@gmail.com"
$env:ADMIN_EMAIL="your-account@gmail.com"
```
Use a Gmail App Password, not your normal account password. Do not commit credentials.

## Quotation pricing
The server calculates all prices from the database. Never trust prices posted by the browser.
- `min_price`: Starter package base price
- `max_price`: Advanced package base price
- Features can be included in Starter and/or Advanced
- Selectable add-ons use `additional_price`
- Custom tier stores the current package range as the estimated range is not a single final quote; the request's estimated_total is initialized to the minimum price and admin should confirm the actual quote.

## Existing project integration
This bundle is a standalone, complete starter project. If merging into an existing Nkript project, do not overwrite your existing database or migrations. Copy the relevant models/views/templates carefully, update the app label if needed, and generate migrations in that project.


## Trichy editorial design & local SEO
The homepage and portfolio have an editorial, typography-led layout inspired by contemporary design portfolios (not a pixel-for-pixel copy). Page metadata and local SEO copy target Trichy/Tiruchirappalli naturally. Review `LOCAL_SEO_LAUNCH_CHECKLIST.md` before deployment. Replace sample domain and contact details with verified business information.
"# Nkript-web" 
