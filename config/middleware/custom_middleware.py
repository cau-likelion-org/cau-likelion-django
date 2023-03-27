class DatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META['HTTP_HOST'] == 'cau-likelion.org':
            request.database = 'chunghaha'
        elif request.META['HTTP_HOST'] == 'dev.cau-likelion.org':
            request.database = 'dev_chunghaha'
        else:
            request.database = 'default'

        response = self.get_response(request)

        return response