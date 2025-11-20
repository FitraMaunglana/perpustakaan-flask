# Perpustakaan Unik (WebServer3)

Simple Flask-based library server where administrators can upload PDF files (books, articles, tasks) and users can read, download, and comment.

Quick start

1. Install Python 3.8+ and create a virtualenv (recommended).
2. Install deps:

```bash
python3 -m pip install -r /opt/perpustakaan/requirements.txt
```

3. Initialize the database:

```bash
python3 /opt/perpustakaan/init_db.py
```

4. Set an admin password (environment variable). Default is `admin` if not set. For example:

```bash
export ADMIN_PASS="s3cret"
```

5. Run the server:

```bash
python3 /opt/perpustakaan/app.py
```

Open http://localhost:8000

Notes
- Admin: go to /admin/login and enter ADMIN_PASS to access upload page.
- Uploads are stored in `/opt/perpustakaan/uploads`.
- This is a minimal prototype intended for local testing. For production, serve uploads via a webserver and secure admin authentication.
