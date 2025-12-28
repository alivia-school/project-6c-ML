# import flask app but need to call it "application" for WSGI to work
from flask_app import app as application

if __name__ == '__main__':
    application.run(debug=True)