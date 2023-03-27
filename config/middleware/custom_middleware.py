from django.utils.deprecation import MiddlewareMixin
import logging

class SetDatabaseMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
    
        logger.warning(request.META['HTTP_REFERER'])
    
        stream_handler = logging.StreamHandler()
        logger.addHandler(stream_handler)
        
        if 'HTTP_REFERER' in request.META:
            referer = request.META['HTTP_REFERER']
            if 'cau-likelion.org' in referer:
                request.session['database'] = 'chunghaha'
            elif 'dev.cau-likelion.org' in referer:
                request.session['database'] = 'chunghaha-dev'
        return None