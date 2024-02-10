from django.http import HttpResponse

class JavaScriptContentTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 200 and response['Content-Type'] == 'text/plain' and request.path.endswith('.js'):
            response['Content-Type'] = 'application/javascript;charset=utf-8'
        return response