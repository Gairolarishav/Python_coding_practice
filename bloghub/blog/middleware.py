import time

class RequestTimingMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response   # runs once at server start


    def __call__(self,request):
        start = time.time()

        print(request.user)
        response = self.get_response(request)   # the view runs here
          
        ms = (time.time() - start) * 1000  # After the view
        response["X-Time-Ms"] = f"{ms:1f}"
        print(f"[middleware] {request.method} {request.path} -> {response.status_code} ({ms:.1f} ms)")
        return response