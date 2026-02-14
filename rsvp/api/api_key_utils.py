from ninja.security import APIKeyHeader
import os

class APIKeyHeaderSecurity(APIKeyHeader):
    param_name = "x-api-key"

    def authenticate(self, request, key):
        expected_key = os.getenv("API_KEY")
        if key == expected_key:
            return key  # return something truthy
        return None

api_key_security = APIKeyHeaderSecurity()
