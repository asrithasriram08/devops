import random
import socket
from datetime import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)

ITEMS = ["Smartphone", "Shoes", "Headphones", "Laptop"]


def pod_name():
    return socket.gethostname()


def current_time():
    return datetime.now().strftime("%H:%M:%S")


@app.get("/")
def home():
    return jsonify(
        message="Welcome to Big Sale!",
        pod=pod_name(),
        ts=datetime.now().isoformat(timespec="seconds"),
    )


@app.get("/buy")
def buy():
    user = request.args.get("user") or f"user-{random.randint(1000, 9999)}"
    return jsonify(
        status="success",
        item=random.choice(ITEMS),
        user=user,
        served_by_pod=pod_name(),
        time=current_time(),
    )


@app.get("/health")
def health():
    return jsonify(status="healthy", pod=pod_name())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
