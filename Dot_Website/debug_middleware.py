import traceback


class CaptureExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        request._error_traceback = "".join(
            traceback.format_exception(type(exception), exception, exception.__traceback__)
        )
        return None
