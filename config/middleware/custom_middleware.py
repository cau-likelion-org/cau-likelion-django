import logging

class DatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #logging
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.warning(request.META['HTTP_HOST'])
        stream_handler = logging.StreamHandler()
        logger.addHandler(stream_handler)
        
        if request.META['HTTP_HOST'] == 'cau-likelion.org' or 'api-cau-likelion.shop':
            request.database = 'chunghaha'
        elif request.META['HTTP_HOST'] == 'dev.cau-likelion.org':
            request.database = 'chunghaha-dev'
        else:
            request.database = 'default'

        response = self.get_response(request)

        return response