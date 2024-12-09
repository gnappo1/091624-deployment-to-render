from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from os import environ


app = Flask(
    __name__,
    static_url_path="",
    static_folder="../client/build",
    template_folder="../client/build",
)

@app.route("/")
@app.route("/productions/<int:id>")
@app.route("/productions/<int:id>/edit")
@app.route("/productions/new")
@app.route("/registration")
def index(id=0):
    return render_template("index.html")


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SESSION_TYPE"] = "sqlalchemy"

if environ.get("FLASK_ENV") == "production":
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("POSTGRESQL_DATABASE_URI")
elif environ.get("FLASK_ENV") == "development":
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("SQLITE_DATABASE_URI")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("SQLITE_TEST_DATABASE_URI")


app.secret_key = environ.get("SESSION_SECRET")
# flask-sqlalchemy connection to app
db = SQLAlchemy(app)
app.config["SESSION_SQLALCHEMY"] = db
# flask-migrate connection to app
migrate = Migrate(app, db)
# flask-restful connection to app
api = Api(app, prefix="/api/v1")
flask_bcrypt = Bcrypt(app)
Session(app)
