# -*- coding: utf-8 -*-


class LemonwayError(Exception):
    def __init__(self, message=None, code=None, *args, **kwargs):
        super(LemonwayError, self).__init__(message, *args, **kwargs)
        self.message = message
        self.code = code
