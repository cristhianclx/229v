from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/data")
def data():
    return "<p>DATA :)<p>"

@app.route("/students")
def students():
    return [{
        "id": 123,
        "name": "abc"
    }, {
        "id": 456,
        "name": "def"
    }]

@app.route("/students/<int:id>")
def students_by_id(id):
    return {
        "id": id,
        "name": "abc"
    }


data = [{
    "user": "frank",
    "password": "123456",
}, {
    "user": "cristhian",
    "password": "123123",
}, {
    "user": "raul",
    "password": "12345678",
}]


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return "you need to login"
    if request.method == "POST":
        raw = request.get_json()
        user = raw.get("user") # raw["user"]
        password = raw.get("password")
        if user and password:
            for r in data:
                if r["user"] == user and r["password"] == password:
                    return "valid login"
            return "invalid login"
        else:
            return "missing data"