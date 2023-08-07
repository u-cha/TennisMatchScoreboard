import typing


class Response:
    def __init__(self):
        self.status: str = '200 OK'
        self.headers: typing.List[typing.Tuple] = [("Content-Type", "text/html")]
        self.__body: bytes = "".encode("utf-8")

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, content):
        self.__body = content.encode("utf-8")
