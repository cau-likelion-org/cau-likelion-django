from django.conf import settings
from django.db import connections

import logging


class SetDatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.META.get('HTTP_REFERER')
        backend = request.META.get('HTTP_HOST')
        
         # 로그 console 출력
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
        logger.warning(host)

        stream_handler = logging.StreamHandler()
        logger.addHandler(stream_handler)
        
        if host == 'https://cau-likelion.org/' or backend == 'api-cau-likelion.shop':
            db_name = 'chunghaha'
        elif host == 'https://dev.cau-likelion.org/':
            db_name = 'chunghaha-dev'
        else:
            db_name = 'default'
        
        # 동적으로 DB 설정 변경
        settings.DATABASES['default'] = settings.DATABASES[db_name]

        response = self.get_response(request)

        return response
    
   