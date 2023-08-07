from response import Response
from View.jinja import View


class Handler:
    def __init__(self, environ):
        self.response = Response()
        self.environ = environ

    def perform(self):
        request_method = self.environ.get("REQUEST_METHOD")
        if request_method == "GET":
            self.perform_get()
            return
        if request_method == "POST":
            self.perform_post()
            return
        # это заглушка на случай, если будет другой метод http запроса
        body = View.render('index')
        self.response.body = body

    def perform_get(self):
        pass

    def perform_post(self):
        pass
