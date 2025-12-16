"""
WSGI config for PythonAnywhere deployment
"""
from flames_app.app import app as application

if __name__ == "__main__":
    application.run()
