import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return os.getenv("APP_MESSAGE", "default message")


@app.route("/secret")
def secret():
    return os.getenv("SECRET_TOKEN", "no secret")


@app.route("/health")
def health():
    return "Ok"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
