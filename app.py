from flask import Flask, request
import os

app = Flask(__name__)

# VULNERABILITY 1: hardcoded secret
app.config["SECRET_KEY"] = "super-hardcoded-secret"

# VULNERABILITY 2: weak input handling
@app.route("/")
def home():
    name = request.args.get("name", "guest")
    return f"Hello {name}"

# VULNERABILITY 3: debug info style route
@app.route("/config")
def config():
    return {
        "debug": True,
        "secret_key": app.config["SECRET_KEY"],
        "env_message": os.getenv("APP_MESSAGE", "not-set")
    }

if __name__ == "__main__":
    # VULNERABILITY 4: debug mode enabled
    app.run(host="0.0.0.0", port=5000, debug=True)
