from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://postgres:sistemas@127.0.0.1:5432/instance"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    age = db.Column(db.Integer)
    bank = db.Column(db.String(10))
    country = db.Column(db.String(15))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<User {}>".format(self.id)


class Message(db.Model):
    
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<Message {}>".format(self.id)


@app.route("/")
def index():
    return {
        "status": "healthy"
    }