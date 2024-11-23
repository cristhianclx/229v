from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_socketio import SocketIO
import enum
from sqlalchemy import Enum


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.config['SECRET_KEY'] = 'TOP-SECRET'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

socketio = SocketIO(app)


class MessageImportance(enum.Enum):
    LOW = "LOW"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    importance = db.Column(Enum(MessageImportance))
    feedback = db.Column(db.String(150))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Message {self.id}>"


@app.route("/")
def index():
    messages = Message.query.all()
    return render_template("index.html", messages=messages)


@socketio.on("ws-welcome")
def handle_ws_welcome(data):
    print("data in ws-welcome: " + str(data))


@socketio.on("ws-messages")
def handle_ws_messages(data):
    message = Message(**data)
    db.session.add(message)
    db.session.commit()
    is_important = False
    if data.get("importance", "") == "high" or "URGENT" in data.get("feedback", ""):
        is_important = True
    data["is_important"] = is_important
    socketio.emit("ws-messages-responses", data)