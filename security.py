import time
from flask import request, jsonify
from functools import wraps

API_KEYS = {"your_api_key": True}  # Replace with your valid API keys

# Rate limiting configuration
RATE_LIMIT = 5  # requests allowed per timeframe
TIMEFRAME = 60  # time in seconds
request_counts = {}

# Decorator for API key validation
def requires_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if not api_key or api_key not in API_KEYS:
            return jsonify({'message': 'Invalid API key!'}), 403
        return f(*args, **kwargs)
    return decorated

# Decorator for rate limiting
def rate_limiter(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        client_ip = request.remote_addr
        current_time = time.time()
        if client_ip not in request_counts:
            request_counts[client_ip] = []
        # Remove requests that are outside the timeframe
        request_counts[client_ip] = [timestamp for timestamp in request_counts[client_ip] if current_time - timestamp < TIMEFRAME]
        if len(request_counts[client_ip]) >= RATE_LIMIT:
            return jsonify({'message': 'Rate limit exceeded!'}), 429
        request_counts[client_ip].append(current_time)
        return f(*args, **kwargs)
    return decorated

# Example API endpoint usage
@requires_api_key
@rate_limiter
def my_api_endpoint():
    return jsonify({'message': 'Success!'})

# Don't forget to integrate this with your Flask app!