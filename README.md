# H‑24 Blog

A lightweight, secure-minded Flask blog application for publishing short-form posts, managing user profiles, and verifying users via transactional email. Built as a learning project and suitable as a starting point for small community blogs or prototypes.

Badges
- Build / CI: (add your CI badge)
- License: MIT (or choose your license)
- Status: Prototype / Active development

---

## Table of contents
- [Key features](#key-features)
- [Architecture & stack](#architecture--stack)
- [Quickstart (development)](#quickstart-development)
- [Configuration](#configuration)
- [Running & deployment notes](#running--deployment-notes)
- [Security considerations (production checklist)](#security-considerations-production-checklist)
- [Testing & quality](#testing--quality)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Roadmap — Future functions & new ideas](#roadmap---future-functions--new-ideas)
- [License](#license)
- [Maintainer](#maintainer)

---

## Key features
- User registration and login (Flask-Login)
- Email verification via Brevo (Sendinblue transactional API)
- Profile pictures hosted on Cloudinary
- Create, edit, and view posts with simple caching for latest posts
- Rate limiting on sensitive endpoints (Flask-Limiter)
- Basic security headers (CSP frame-ancestors, X-Frame-Options)

---

## Architecture & stack
- Language: Python 3.10+
- Framework: Flask
- Persistence: SQLAlchemy (Postgres recommended)
- Image hosting: Cloudinary
- Email: Brevo (sib_api_v3_sdk)
- Caching: Flask-Caching (redis or simple)
- Rate limiting: Flask-Limiter
- Auth: Flask-Login, bcrypt for password hashing
- Key modules:
  - app/__init__.py — app and extension setup
  - app/routes.py — HTTP routes & business logic
  - app/models.py — SQLAlchemy models (User, Post)
  - app/forms.py — WTForms definitions
  - app/utils.py — email, token, and caching helpers

---

## Quickstart (development)
1. Clone and create a virtual environment:
   ```bash
   git clone https://github.com/prajapatiHardik2008/H-24_Blog.git
   cd H-24_Blog
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Set required environment variables (example .env file or export in shell):
   ```
   SECRET_KEY=your_secret_key
   SECURITY_SALT=your_security_salt
   DB_URL=postgresql://user:pass@host:5432/dbname
   BREVO_API=your_brevo_api_key
   CLOUDINARY_CLOUD_NAME=...
   CLOUDINARY_API_KEY=...
   CLOUDINARY_API_SECRET=...
   MAIL_USERNAME=...
   MAIL_PASSWORD=...
   CACHE_TYPE=simple
   REDIS_URL=redis://localhost:6379
   ```

3. Initialize the database (development):
   - Option A (quick, not for production): open a Python shell and run:
     ```python
     from app import db, app
     with app.app_context():
         db.create_all()
     ```
   - Recommended: integrate Flask-Migrate and maintain migrations.

4. Run locally:
   ```bash
   python run.py
   # or
   FLASK_APP=run.py flask run
   ```

5. Open http://127.0.0.1:5000

---

## Configuration (env vars & purpose)
- SECRET_KEY — Flask secret for session and CSRF signing (required)
- SECURITY_SALT — salt used for email verification tokens (required)
- DB_URL — SQLAlchemy database URL (Postgres recommended)
- BREVO_API — Brevo transactional email API key (or other provider)
- CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET — Cloudinary credentials
- MAIL_USERNAME, MAIL_PASSWORD — optional SMTP credentials for Flask-Mail fallback
- CACHE_TYPE — e.g., "redis" or "simple" for development
- REDIS_URL — required if CACHE_TYPE=redis or for Flask-Limiter storage

Ensure these values are never committed to source control. Use a secrets manager for production.

---

## Running & deployment notes
- Use a WSGI server (gunicorn/uvicorn) behind a reverse proxy (Nginx) with HTTPS.
- Set environment variables in your hosting platform or CI/CD pipeline (do not use .env files in production).
- Configure HSTS and set secure cookie flags. Example production config:
  ```python
  app.config.update(
      SESSION_COOKIE_SECURE=True,
      SESSION_COOKIE_HTTPONLY=True,
      REMEMBER_COOKIE_SECURE=True,
      SESSION_PROTECTION='strong'
  )
  ```
- Use a managed Postgres instance for reliability; run schema migrations via Flask-Migrate.

---

## Security considerations (production checklist)
- Fail-fast on missing secrets (raise on startup if SECRET_KEY/SECURITY_SALT/DB_URL are not set).
- Enforce HTTPS and set HSTS headers.
- Harden Content-Security-Policy (CSP) beyond frame-ancestors; allow scripts/styles only from trusted sources.
- Validate and sanitize post content (use Bleach to whitelist tags and attributes).
- Validate and restrict file uploads (MIME type, size limits); require authentication for upload endpoints and use signed uploads where possible.
- Validate redirect targets (protect against open redirect attacks).
- Rate-limit authentication endpoints and implement account lockout thresholds after repeated failed attempts.
- Avoid returning raw exception messages to users; log detailed errors server-side and present generic messages client-side.
- Rotate API keys and store them in a secrets manager (AWS Secrets Manager, Vault, etc.).
- Add server-side monitoring and error tracking (Sentry) and audit logging.

---

## Testing & quality
- Add unit and integration tests (pytest) for:
  - Authentication flows (register, login, verify)
  - Post CRUD operations
  - Upload image endpoint validation
- Add linting (flake8/ruff) and type checking (mypy) as part of CI.
- Add GitHub Actions workflow for tests and linting.

---

## Troubleshooting
- App fails to start: check that required env vars (SECRET_KEY, SECURITY_SALT, DB_URL) are set and valid.
- Email not sent: verify BREVO_API key and that external network access is allowed. Check logs for API errors.
- Images not loading: confirm Cloudinary credentials and that image URLs returned are secure (https).
- Database errors: ensure DB_URL is correct and database exists; run migrations or db.create_all() in dev.

---

## Contributing
- Fork the repo and open a pull request for changes.
- Add tests for bug fixes and new features.
- Follow the coding style and include descriptive commit messages.
- For major features, open an issue first to discuss design and scope.

---

## Roadmap — Future functions & new ideas
Prioritized improvements and feature ideas you can track/implement:
1. Moderation & admin dashboard (reports, remove posts, ban users)
2. Comments & threaded replies with moderation tools
3. Reactions (likes) and simple analytics (views)
4. Follow/unfollow users and personalized feed (fanout or pull model)
5. Markdown editor with server-side sanitization and image embedding
6. OAuth social login (GitHub, Google) and optional 2FA (TOTP)
7. Drafts, scheduled posts, and post tagging/filters
8. Full-text search (Postgres full-text or external index)
9. Public REST API with API keys and rate limits
10. CI/CD, automated tests, and Sentry integration for error monitoring

---


---

## Maintainer
Hardik Prajapati — repository owner / maintainer  
Contact: hardikprajapati2008@gmail.com


---

If you'd like, I can:
- Commit this README to the repo in a PR.
- Create a patch that fixes the `app/utils.py` import and the open-redirect in login.
- Add a starter GitHub Actions workflow for testing and linting.

Which of these would you like next?
