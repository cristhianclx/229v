from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.config['SECRET_KEY'] = 'TOP-SECRET'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

socketio = SocketIO(app)


class Room(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    messages = db.relationship("Message", back_populates="room")

    def __repr__(self):
        return f"<Room {self.id}>"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    room_id = db.Column(db.String, db.ForeignKey("room.id"))
    room = db.relationship("Room", backref="room")

    def __repr__(self):
        return f"<Message {self.id}>"


@app.route("/")
def index():
    rooms = Room.query.all()
    data = []
    for r in rooms:
        participants = len(db.session.query(Message.nickname, db.func.count(Message.nickname)).filter(Message.room_id == r.id).group_by(Message.nickname).all())
        data.append({
            "room": r,
            "participants": participants,
        })
    return render_template("index.html", data = data)


@app.route("/rooms/create", methods=["GET", "POST"])
def rooms_create():
    if request.method == "GET":
        return render_template("rooms-create.html")
    if request.method == "POST":
        room = Room(
            id = request.form["id"],
            name = request.form["name"],
        )
        db.session.add(room)
        db.session.commit()
        return redirect(url_for('rooms', id=room.id))


@app.route("/rooms/<id>")
def rooms(id):
    room = Room.query.filter_by(id = id).first()
    messages = Message.query.filter_by(room = room)
    participants = len(db.session.query(Message.nickname, db.func.count(Message.nickname)).filter(Message.room_id == room.id).group_by(Message.nickname).all())
    return render_template("room.html", room=room, messages=messages)


@socketio.on("ws-messages")
def handle_ws_messages(data):
    message = Message(**data)
    db.session.add(message)
    db.session.commit()
    socketio.emit("ws-messages-{}".format(message.room.id), data)


# rooms - add column max_participants, default=10
# when you want to enter or join a room, if max_participants >= participants