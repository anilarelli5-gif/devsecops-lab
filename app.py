import os,time
from flask import Flask, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# 🔥 Metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'Request latency'
)

# 🔹 Routes
@app.route("/")
def home():
    return os.getenv("APP_MESSAGE", "default message")

@app.route("/secret")
def secret():
    return os.getenv("SECRET_TOKEN", "no secret")

@app.route("/health")
def health():
    return "Ok"

# 🔥 Metrics endpoint
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


# 🔥 Track metrics for every request
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    REQUEST_LATENCY.observe(time.time() - request.start_time)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
