from weddindInvitation import initialize_csv, app

# Ensure CSV exists before the app starts handling requests
initialize_csv()

# Expose the WSGI application for servers like gunicorn
application = app
