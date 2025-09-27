from django.http import JsonResponse
from decouple import config


class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.secure_token = config("API_KEY")

    def __call__(self, request):
        # API Key in the request's headers
        request_token = request.headers.get('X-Api-Key')

        # No valid Key
        if not request_token or request_token != self.secure_token:
            return JsonResponse({"status": "error", "message": "Forbidden Access"}, status=401)

        # Valid Key
        response = self.get_response(request)
        return response