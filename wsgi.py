from weddindInvitation import app

# The app module now initializes its database on import. Expose the
# WSGI application for servers like gunicorn.
application = app
