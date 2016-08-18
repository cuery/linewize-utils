class Request:
    request_uri = None
    args = None
    response = None

    def __init__(self, request_uri, args, response=None):
        self.request_uri = request_uri
        self.args = args
        self.response = response

    def __str__(self):
        return "Request({}, {}, {})".format(self.request_uri, self.args, self.response)

    def __repr__(self):
        return str(self)


class ConnectionMock:
    conditions = []
    requests = []

    def __init__(self):
        self.requests = []
        self.conditions = []

    def request(self, url, args):
        # add to the requests list - this is used by assert
        self.requests.append(Request(url, args))

        # respond
        for condition in self.conditions:
            if condition.request_uri == url:
                return condition.response

    def when(self, request_uri, with_args=None, response=None):
        self.conditions.append(Request(request_uri, with_args, response))

    def has(self, request_url, args):
        for request in self.requests:
            if request.request_uri == request_url and request.args == args:
                return True
        return False
