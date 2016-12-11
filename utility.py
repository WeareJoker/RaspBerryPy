# coding: utf-8
def ether2data(ether):
    proto = ether.child().child()
    return proto.child()


def get_data_payload(data):
    return data.get_buffer_as_string()


class NoInfoException(Exception):
    pass


class InvalidInfoException(Exception):
    pass


class HTTPRequest:
    def __init__(self, payload):
        self.payload = payload
        self.request_object = self.get_http_request_object_list()
        self._cookie = None
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

    @property
    def cookie(self):
        if self._cookie is None:
            self._cookie = self.get_cookie()

        return self._cookie
