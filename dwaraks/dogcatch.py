from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

register(set_global_tracer_provider=False)
SmolagentsInstrumentor().instrument()