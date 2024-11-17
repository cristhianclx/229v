from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(15), nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<User {} {}>".format(self.first_name, self.last_name)


class Message(db.Model):
    
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="user")

    def __repr__(self):
        return "<Message {}>".format(self.title)


@app.route("/ping")
def ping():
    return {
        "status": "healthy"
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/users")
def users():
    data = User.query.all()
    return render_template("users.html", items=data)


@app.route("/users/add", methods=["GET", "POST"])
def users_add():
    if request.method == "GET":
        return render_template("users-add.html")
    if request.method == "POST":
        user = User(
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            age=request.form["age"],
            country=request.form["country"],
            content=request.form["content"],
        )
        db.session.add(user)
        db.session.commit()
        return render_template("users-add.html", message="User saved")
    

@app.route("/users/<id>")
def users_by_id(id):
    data = User.query.get_or_404(id)
    return render_template("users-detail.html", item=data)


@app.route("/users/edit/<id>", methods=["GET", "POST"])
def users_edit_by_id(id):
    data = User.query.get_or_404(id)
    if request.method == "GET":
        return render_template("users-edit.html", item=data)
    if request.method == "POST":
        data.first_name = request.form["first_name"]
        data.last_name = request.form["last_name"]
        data.age = request.form["age"]
        data.country = request.form["country"]
        data.content = request.form["content"]
        db.session.add(data)
        db.session.commit()
        return render_template("users-edit.html", item=data, message="User updated")


@app.route("/users/delete/<id>", methods=["GET", "POST"])
def users_delete_by_id(id):
    data = User.query.get_or_404(id)
    if request.method == "GET":
        return render_template("users-delete.html", item=data)
    if request.method == "POST":
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('users'))
    

@app.route("/users/<user_id>/messages/add", methods=["GET", "POST"])
def users_by_id_add_message(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "GET":
        return render_template("messages-add.html", user=user)
    if request.method == "POST":
        message = Message(
            title=request.form["title"],
            content=request.form["content"],
            user=user,
        )
        db.session.add(message)
        db.session.commit()
        return render_template("messages-add.html", user=user, message="Message saved")
    

@app.route("/users/<user_id>/messages")
def users_by_id_messages(user_id):
    user = User.query.get_or_404(user_id)
    items = Message.query.filter_by(user = user).all()
    return render_template("messages.html", items=items, user=user)
