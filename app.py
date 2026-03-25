from flask import Flask
import os

app = Flask(__name__)

APP_MESSAGE = os.getenv("APP_MESSAGE", "Hello DevSecOps")
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "not-set")

@app.route('/')
def home():
    return APP_MESSAGE

@app.route('/health')
def health():
    return "OK"

@app.route('/secret-check')
def secret_check():
    if SECRET_TOKEN == "not-set":
        return "Secret missing", 500
    return "Secret loaded", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
