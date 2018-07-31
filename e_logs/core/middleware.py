from django.http import HttpResponse
import logging
import sys


class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        pass


class StdLogger(object):
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())  # somehow this line leads to stakowerflow

    def flush(self):
        pass


stdout_logger = StdLogger(logging.getLogger('STDOUT'), logging.INFO)
sys.stdout = stdout_logger

stderr_logger = StdLogger(logging.getLogger('STDERR'), logging.ERROR)
sys.stderr = stderr_logger
