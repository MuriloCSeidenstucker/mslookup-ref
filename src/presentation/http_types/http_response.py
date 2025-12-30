# pylint: disable=C0301:line-too-long, R0903:too-few-public-methods


class HttpResponse:

    def __init__(self, status_code, body) -> None:
        self.status_code = status_code
        self.body = body
