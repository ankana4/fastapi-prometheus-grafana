from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Response, Request

REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total API Requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "Api request latency",
    ["endpoint"]
)
USER_CREATED_TOTAL = Counter(
    "users_created_total",
    "Total number of users successfully created"
)

USER_CREATE_FAILED_TOTAL = Counter(
    "users_create_failed_total",
    "Total number of failed user creation attempts",
    ["reason"]
)

def setup_metrics(app):
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        endpoint = request.url.path
        REQUEST_COUNT.labels(request.method, endpoint).inc()
        
        with REQUEST_LATENCY.labels(endpoint).time():
            response = await call_next(request)
        return response
    
    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(), media_type="text/plain")    