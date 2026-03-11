import json

class Storage:
    def __init__(self):
        self.in_memory_storage = {}
        self.persistent_storage_file = 'storage.json'
        self.load_persistent_storage()

    def load_persistent_storage(self):
        try:
            with open(self.persistent_storage_file, 'r') as file:
                self.in_memory_storage.update(json.load(file))
        except FileNotFoundError:
            pass  # If the file doesn't exist, we just continue with in-memory storage

    def save_persistent_storage(self):
        with open(self.persistent_storage_file, 'w') as file:
            json.dump(self.in_memory_storage, file)

    def add_api_key(self, user_id, api_key):
        self.in_memory_storage[user_id] = api_key
        self.save_persistent_storage()

    def get_api_key(self, user_id):
        return self.in_memory_storage.get(user_id)

class RequestTracker:
    def __init__(self):
        self.requests = []

    def track_request(self, user_id, request_details):
        self.requests.append({'user_id': user_id, 'request_details': request_details})

    def get_request_log(self):
        return self.requests

# Example usage:
# storage = Storage()
# storage.add_api_key('user1', 'apikey123')
# tracker = RequestTracker()
# tracker.track_request('user1', 'GET /api/resource')