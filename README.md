# Wedding Invitation App

This is a small Flask app that serves a wedding invitation site and captures RSVPs to a CSV file.

Quick local run (venv):

```bash
cd /path/to/repo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python start_server.py
# open http://127.0.0.1:5001
```

Deploying to Render / Railway / Heroku

1. Push this repository to GitHub.
2. On Render (recommended):
   - Create a new "Web Service" and connect your GitHub repo.
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command (Render) or use the Procfile: `gunicorn wsgi:application -b 0.0.0.0:$PORT -w 4`
   - Add any needed environment variables (SECRET_KEY, ADMIN_PASSWORD, SMTP credentials if using email scripts).

3. On Heroku: the included `Procfile` will make Heroku run `gunicorn wsgi:application` automatically.

Expose locally (temporary sharing)

If you want to test with friends before deploying, run your server locally and expose it with ngrok:

```bash
# in one terminal, run the app
python start_server.py
# in another
ngrok http 5001
# share the https://...ngrok.io URL
```

Notes and next steps

- RSVPs are stored in `rsvp_responses.csv` in the repository root.
- If you want me to add email sending (SendGrid/Gmail), prefilled RSVP links, or an admin view to download RSVPs, say which and I can add it.
