import logging
import settings

class SetDatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.META.get('HTTP_REFERER')
        
        if host == 'https://cau-likelion.org/':
            db_name = 'chunghaha'
        elif host == 'https://dev.cau-likelion.org/':
            db_name = 'chunghaha-dev'
        else:
            db_name = None
        
        if db_name:
            settings.DATABASE_ROUTERS = ['config.routers.DatabaseRouter']
            settings.DATABASES[db_name]['ATOMIC_REQUESTS'] = True
        
        response = self.get_response(request)

        return response