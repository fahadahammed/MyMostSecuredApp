from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest
import jwt
import os

app = Flask(__name__)

SECRET_KEY = os.getenv('SECRET_KEY')

@app.route("/", methods=["GET"])
def the_root():
    return jsonify(
            {
                "msg": "Welcome to Most Secured Application !"
            }
        )

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if username == os.getenv("USERNAME", 'admin') and \
        password == os.getenv("PASSWORD", 'admin123'):
        token = jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token}), 200
    else:
        raise BadRequest("Invalid credentials")

@app.route("/protected")
def protected():
    token = request.headers.get("Authorization")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("username")
        return jsonify({"message": f"Welcome, {username}!"}), 200
    except jwt.ExpiredSignatureError:
        raise BadRequest("Token has expired")
    except jwt.InvalidTokenError:
        raise BadRequest("Invalid token")

if __name__ == "__main__":
    app.run(debug=False)