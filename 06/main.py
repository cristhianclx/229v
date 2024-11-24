from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

api = Api(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<User {}>".format(self.id)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="user")

    def __repr__(self):
        return "<Message {}>".format(self.id)


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "name",
            "age",
            "bio",
            "created_at",
        )
        model = User
        datetimeformat = "%Y-%m-%d %H:%M:%S"


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class MessageSimpleSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "content",
            "created_at",
        )
        model = Message
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_simple_schema = MessageSimpleSchema()
messages_simple_schema = MessageSimpleSchema(many=True)


class MessageSchema(ma.Schema):
    user = ma.Nested(UserSchema)

    class Meta:
        fields = (
            "id",
            "content",
            "created_at",
            "user",
        )
        model = Message
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)


class PINGResource(Resource):
    def get(self):
        return {"status": "healthy"}


class UsersResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)
        # data = []
        # for u in users:
        #     data.append({
        #         "id": u.id,
        #         "name": u.name,
        #         "age": u.age
        #     })
        # return data

    def post(self):
        data = request.get_json()
        user = User(**data)  # User(name = data["name"], age=data["age"])
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201
        # return {
        #     "id": user.id,
        #     "name": user.name,
        #     "age": user.age
        # }, 201


class UserIDResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        return user_schema.dump(user)
        # return {
        #     "id": user.id,
        #     "name": user.name,
        #     "age": user.age
        # }

    def patch(self, id):
        user = User.query.get_or_404(id)
        data = request.get_json()
        user.name = data.get("name", user.name)
        user.age = data.get("age", user.age)
        user.bio = data.get("bio", user.bio)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user)
        # return {
        #     "id": user.id,
        #     "name": user.name,
        #     "age": user.age
        # }

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {}, 204


class UserIDMessagesResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        messages = Message.query.filter_by(user=user).all()
        return messages_simple_schema.dump(messages)


class MessagesResource(Resource):
    def get(self):
        messages = Message.query.all()
        return messages_schema.dump(messages)

    def post(self):
        data = request.get_json()
        message = Message(**data)
        db.session.add(message)
        db.session.commit()
        return message_schema.dump(message), 201


api.add_resource(PINGResource, "/")
api.add_resource(UsersResource, "/users")
api.add_resource(UserIDResource, "/users/<id>")
api.add_resource(UserIDMessagesResource, "/users/<id>/messages")
api.add_resource(MessagesResource, "/messages")
