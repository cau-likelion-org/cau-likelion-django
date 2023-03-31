from django.conf import settings
from django.db import connections

import logging


class SetDatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.META.get('HTTP_REFERER')
        backend = request.META.get('HTTP_HOST')
        
        if host == 'https://cau-likelion.org/' :
            db_name = 'chunghaha'
        elif host == 'https://dev.cau-likelion.org/':
            db_name = 'chunghaha-dev'
        elif backend == 'api-cau-likelion.shop': # 배포 서버에서 DB 확인 위해 추가
            db_name = 'chunghaha'
        else:
            db_name = 'default'

        print(db_name)
        # 동적으로 DB 설정 변경
        settings.DATABASES['default'] = settings.DATABASES[db_name]

        response = self.get_response(request)

        return response
    
   