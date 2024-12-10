from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from os import environ
from datetime import timedelta

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

if environ.get("FLASK_ENV") == "production":
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("POSTGRESQL_DATABASE_URI")
elif environ.get("FLASK_ENV") == "development":
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("SQLITE_DATABASE_URI")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("SQLITE_TEST_DATABASE_URI")

# flask-jwt-extended configuration
app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_CSRF_PROTECTION"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=2)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)


# flask-jwt-extended connection to app
jwt = JWTManager(app)
db = SQLAlchemy(app)
# flask-migrate connection to app
migrate = Migrate(app, db)
# flask-restful connection to app
api = Api(app, prefix="/api/v1")
flask_bcrypt = Bcrypt(app)
# Session(app)
