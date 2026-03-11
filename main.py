from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
import time
from datetime import datetime, timedelta
from collections import defaultdict

app = FastAPI()

API_KEY = "your_api_key"
API_KEY_HEADER = APIKeyHeader(name="X-API-KEY")

# In-memory store for API keys and their expiration time
api_keys = {}  # to track API keys
rate_limits = defaultdict(lambda: {'requests': 0, 'last_request_time': time.time()})  # track requests per key
REQUEST_LIMIT = 5  # max requests per minute

# Generate an API key with a specific expiration time
@app.post("/generate_api_key/")
async def generate_api_key():
    key = str(datetime.now().timestamp()).replace('.', '')  # simple key generation
    expiration = datetime.utcnow() + timedelta(hours=1)  # valid for 1 hour
    api_keys[key] = expiration
    return {"api_key": key, "expires_at": expiration}

# Validate the API key
async def validate_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if api_key not in api_keys:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    if datetime.utcnow() > api_keys[api_key]:
        raise HTTPException(status_code=403, detail="API Key has expired")

# Rate limited endpoint
@app.get("/items/")
async def read_items(api_key: str = Depends(validate_api_key)):
    current_time = time.time()
    if rate_limits[api_key]['last_request_time'] < current_time - 60:
        rate_limits[api_key] = {'requests': 0, 'last_request_time': current_time}
    if rate_limits[api_key]['requests'] >= REQUEST_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded").
    rate_limits[api_key]['requests'] += 1
    return {"message": "This is your item."}

# Track requests
@app.middleware("http")
def request_counter(request, call_next):
    api_key = request.headers.get("X-API-KEY")
    if api_key in api_keys:
        print(f"Request received with API key: {api_key}")
    response = call_next(request)
    return response

# Run with: uvicorn main:app --reload
