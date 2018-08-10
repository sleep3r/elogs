import json

from e_logs.core.utils.loggers import default_logger


class SemanticError(Exception):
    def __init__(self, **kwargs):
        self.my_args = kwargs

    def __str__(self):
        if self.my_args.get('code') is not None:
            return json.dumps({'error': self.my_args['code']})
        elif self.my_args.get('message') is not None:
            return json.dumps({"error": "error", "message": self.my_args['message']})
        else:
            default_logger.error(self.my_args)
            return '{"error": "fatal"}'


class AccessError(Exception):
    def __init__(self, **kwargs):
        self.my_args = kwargs

    def __str__(self):
        if self.my_args.get('code') is not None:
            return json.dumps({'error': self.my_args['code']})
        elif self.my_args.get('message') is not None:
            return json.dumps({"error": "error", "message": self.my_args['message']})
        else:
            default_logger.error(self.my_args)
            return '{"error": "fatal"}'
