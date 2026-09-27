# Architecture

- `app/server.py`: Python standard-library HTTP service, SQLite storage, static checks and ZIP export.
- `web/index.html`: English personal workspace and accessible dialogs.
- `web/app.js`: project editing, manual ChatGPT exchange, diff review and revision controls.
- `web/styles.css`: responsive desktop and mobile layouts.
- `tests/test_personal.py`: data and HTTP regression tests.
- `tests/browser.cjs`: browser journeys using synthetic responses.

Only three tables exist: projects, versions and requests. Changes use SQLite transactions. Saves and response application require an exact expected revision. Importing a response never mutates the active Skill. Applying a response appends a revision and marks the request applied in the same transaction.

The HTTP service binds to 127.0.0.1, validates the Host and browser Origin, rejects cross-site fetches, requires JSON for mutations, limits request sizes and serves only an explicit static file allowlist. Browser content renders through textContent or escaping. No subprocess, provider API, telemetry or payment SDK exists.

This local trust model does not authenticate other software or people on the same computer. It is unsuitable for shared hosting. The service and file-backed database are designed for individual use, not hostile multi-user workloads.
