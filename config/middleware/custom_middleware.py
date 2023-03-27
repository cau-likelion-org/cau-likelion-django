from django.utils.deprecation import MiddlewareMixin
import logging

class SetDatabaseMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'HTTP_ORIGIN' in request.META:
            origin = request.META['HTTP_ORIGIN']
            
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            logger.warning(origin)
            stream_handler = logging.StreamHandler()
            logger.addHandler(stream_handler)
            
            if 'cau-likelion.org' in origin:
                request.session['database'] = 'chunghaha'
            elif 'dev.cau-likelion.org' in origin:
                request.session['database'] = 'chunghaha-dev'
        return None
