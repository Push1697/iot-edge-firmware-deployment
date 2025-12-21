import time
import random
from flask import Flask, jsonify
from prometheus_client import Counter, Gauge, Histogram, generate_latest

app = Flask(__name__)

data_blob = "X" * 5_000_000

REQUEST_COUNT = Counter("sensor_requests_total", "Total sensor requests")
CPU_SPIKE = Gauge("sensor_cpu_spike", "Simulated CPU spike state")
PROCESS_LATENCY = Histogram("sensor_processing_latency_seconds", "Processing time")
SCRAPE_DURATION = Histogram("sensor_scrape_duration_seconds", "Time spent generating metrics",buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0])

# New custom metrics to count sensor failures
SENSOR_FAILURES = Counter("sensor_failures_total", "Total number of failed sensor reads")

@app.route("/metrics")
def metrics():
    with SCRAPE_DURATION.time():
        start = time.time()
    # as per my obserbation this below loop is not working anything
    # for _ in range(2000000):
    #     pass
        time.sleep(0.002)  # to reduce the load
    # temp_data = data_blob * random.randint(1, 3) # it's unused as everytime the metrics are scraped it's giving memory issue
    PROCESS_LATENCY.observe(time.time() - start)
    CPU_SPIKE.set(random.randint(0, 1))
    # REQUEST_COUNT.inc() = we should not count the metrics scrape as a request
    return generate_latest()

@app.route("/sensor")
def sensor():
    REQUEST_COUNT.inc()  # Count each sensor request

# added this logic to simulate sensor failures
    if random.random() < 0.1:
        SENSOR_FAILURES.inc()
        return jsonify({"error": "sensor disconnected"}), 500

    if random.random() < 0.2:
        return jsonify({"data": data_blob})

    return jsonify({"status": "ok"}) 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
