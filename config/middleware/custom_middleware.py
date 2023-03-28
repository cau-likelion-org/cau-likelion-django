import logging

class SetDatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.META.get('HTTP_REFERER')
        
        # 로그 console 출력
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
        logger.warning(host)
       
        stream_handler = logging.StreamHandler()
        logger.addHandler(stream_handler)
        
        if host == 'https://cau-likelion.org/':
            request.database = 'chunghaha'
        elif host == 'https://dev.cau-likelion.org/':
            request.database = 'dev_chunghaha'
        else:
            request.database = 'default'

        response = self.get_response(request)

        return response