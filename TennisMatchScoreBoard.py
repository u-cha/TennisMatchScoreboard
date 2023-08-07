from waitress import serve
from router import Router


class WSGIApp:

    def __init__(self, environ, start_fn):
        self.environ = environ
        self.start_fn = start_fn

    def __iter__(self):
        handler_class = Router.get_handler_class_by_path(self.environ.get('PATH_INFO', '/'))
        handler = handler_class(self.environ)
        handler.perform()
        response = handler.response
        self.start_fn(response.status, response.headers)
        yield response.body


serve(WSGIApp, host='localhost', port=3000)
