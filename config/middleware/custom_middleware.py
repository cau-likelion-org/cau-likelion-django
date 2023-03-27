from django.utils.deprecation import MiddlewareMixin
import logging

class SetDatabaseMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'HTTP_REFERER' in request.META:
            referer = request.META['HTTP_REFERER']
            if 'cau-likelion.org' in referer:
                request.session['database'] = 'chunghaha'
            elif 'dev.cau-likelion.org' in referer:
                request.session['database'] = 'chunghaha-dev'
        return None