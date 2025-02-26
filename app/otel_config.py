from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import set_tracer_provider, get_tracer
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# OpenTelemetry Tracing Configuration
def setup_tracing():
    trace_provider = TracerProvider(resource=Resource.create({"service.name": "my-fastapi-service"}))
    trace_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)  # OpenTelemetry Collector
    trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
    
    # Set Global Tracer Provider
    set_tracer_provider(trace_provider)
    return get_tracer(__name__)

# OpenTelemetry Auto-Instrumentation
def instrument_app(app):
    FastAPIInstrumentor.instrument_app(app)  # Auto-trace FastAPI requests
    RequestsInstrumentor().instrument()  # Auto-trace HTTP requests
