from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio
import datetime
import random
import uvicorn
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import psutil
from starlette.responses import Response
import os
import sys
from logger import logger #send logs to logger.py
from otel_config import setup_tracing, instrument_app # send logs to otel_config.py
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.metrics import set_meter_provider


app = FastAPI()


tracer = setup_tracing()
instrument_app(app)

# Enable OpenTelemetry Metrics with Prometheus Exporter
reader = PrometheusMetricReader()
provider = MeterProvider(metric_readers=[reader])
set_meter_provider(provider)


@app.get("/")
def read_root():
    return {"message": "Hello, My name is Arshan and I have set up this Opentelemetry Monitoring "}



#You need to expose a special endpoint to expose the metrics on prom sevrer
@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)



LOG_LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]
MESSAGES = [
    "User logged in",
    "Database connection established",
    "Payment processed successfully",
    "API request timeout",
    "New order placed",
    "Cache refreshed",
    "User authentication failed",
]




async def generate_logs():
    yield f"{datetime.datetime.utcnow().isoformat()} [INFO] - Log streaming started\n".encode("utf-8")
    
    while True:
        log = f"{datetime.datetime.utcnow().isoformat()} [{random.choice(LOG_LEVELS)}] - {random.choice(MESSAGES)}\n"
        yield log.encode("utf-8")
        logger.info(log.strip())
        await asyncio.sleep(1)  



@app.get("/logs")
async def stream_logs():
    return StreamingResponse(generate_logs(), media_type="text/plain", status_code=200)





if __name__ == "__main__":
   uvicorn.run(app, port=8000, reload=True)

