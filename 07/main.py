from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance.db"
app.config["JWT_SECRET_KEY"] = "cibertec"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

jwt = JWTManager(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return "<Message {}>".format(self.id)


class MessageSchema(ma.Schema):
    class Meta:
        model = Message
        fields = (
            "id",
            "content",
            "user_id",
            "created_at"
        )
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_schema = MessageSchema()
messages_schema = MessageSchema(many = True)


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "cristhian" or password != "123123":
        return {
            "msg": "Bad username or password",
        }, 401
    else:
        access_token = create_access_token(identity=username)
        return {
            "login": "ok",
            "token": access_token,
        }


@app.route("/public")
def public():
    return {
        "status": "public",
    }


@app.route("/private")
@jwt_required()
def private():
    logged_username = get_jwt_identity()
    return {
        "status": "private",
        "logged_username": logged_username,
    }


@app.route("/messages")
@jwt_required()
def messages():
    data = Message.query.all()
    return messages_schema.dump(data)


@app.route("/me")
@jwt_required()
def me():
    logged_username = get_jwt_identity()
    data = Message.query.filter_by(user_id = logged_username).all()
    return messages_schema.dump(data)