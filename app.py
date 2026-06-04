import os
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
def start_timer():
    request.start_time = REQUEST_LATENCY.time()

@app.after_request
def record_metrics(response):
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        http_status=response.status_code
    ).inc()

    request.start_time.observe_duration()
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
