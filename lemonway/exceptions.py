# -*- coding: utf-8 -*-


class LemonwayError(Exception):
    def __init__(self, message=None, code=None, short_message=None,
                 *args, **kwargs):
        super(LemonwayError, self).__init__(message, *args, **kwargs)
        self.message = message
        self.code = code
        self.short_message = short_message
