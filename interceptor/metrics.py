"""
Authors: Rohini
Date: 2024-06-01
"""
from opentelemetry import trace
from opentelemetry import metrics
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
import os

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# 1. Setup Resources (Metadata about your app)
resource = Resource(attributes={
    SERVICE_NAME: "spiritual-data-hymn-service"
})

# Get OTLP endpoint from environment variables (defaulting to localhost for Jaeger)
otlp_endpoint = os.getenv("OTLP_ENDPOINT", "http://localhost:4317")

# Configure the tracer provider and resources
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "spiritual-hymn-dashboard"})
    )
)
# Configure the OTLP exporter
otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)

# Append the exporter to the tracer provider
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# Example span usage
tracer = trace.get_tracer(__name__)