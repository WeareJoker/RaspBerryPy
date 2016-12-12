import re

import functools


class NoInfoException(Exception):
    pass


class InvalidInfoException(Exception):
    pass


class HTTPRequest:
    def __init__(self, payload):
        self.payload = payload
        self.request_object = self.get_http_request_object_list()
        self._cookie = None
        self._url = None
        self.host = self.get_host()

    def __repr__(self):
        return "<HTTPRequest %s>" % self.host

    def get_http_request_object_list(self):
        return self.payload.split('\r\n')

    def get_host(self):
        for request_object in self.request_object:
            if request_object.startswith("Host: "):
                return request_object.split(' ')[1]
        else:
            raise NoInfoException("No Host!!!")

    def get_cookie(self):
        cookie_head = "Cookie: "

        for obj in self.request_object:
            if obj.startswith(cookie_head):
                try:
                    return dict([(name, data)
                                 for name, data in [cookie.strip().split('=', 1)
                                                    for cookie in obj[len(cookie_head):].split('; ')]])
                except ValueError:
                    raise InvalidInfoException("Invalid Cookie!!!")
        else:
            return False

    def get_url(self):
        return self.host + self.request_object[0].split(' ')[1]

    @property
    def cookie(self):
        if self._cookie is None:
            self._cookie = self.get_cookie()

        return self._cookie

    @property
    def url(self):
        if self._url is None:
            self._url = self.get_url()

        return self._url


def http_request_filter(filter_rule):
    def actual_http_filter(func):

        @functools.wraps(func)
        def wrapper(*args, **_):
            try:
                if args[0].getlayer("TCP").dport != 80:
                    raise AttributeError

                h = HTTPRequest(args[0].getlayer("Raw").load.decode())

            except (NoInfoException, AttributeError):
                return
            else:
                if re.match(filter_rule, h.host) is None:
                    return
                else:
                    return func(h)

        return wrapper

    return actual_http_filter