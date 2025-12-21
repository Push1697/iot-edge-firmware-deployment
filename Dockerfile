# Stage 1 - builder
FROM python:3.10-alpine AS build
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir flask prometheus_client

# Stage 2: Runner (Final Image)
FROM python:3.10-alpine

WORKDIR /app
COPY --from=build /opt/venv /opt/venv
COPY sensor_service.py .
ENV PATH="/opt/venv/bin:$PATH"

RUN adduser -D sensoruser
USER sensoruser

CMD ["python", "sensor_service.py"]