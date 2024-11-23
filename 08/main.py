from flask import Flask, render_template
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


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
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
    socketio.emit("ws-messages-responses", data)


# columns to add:
#   importance: low, high, medium
#   feedback: texto
# if importance is high or feedback contains word "URGENT" put that message in red