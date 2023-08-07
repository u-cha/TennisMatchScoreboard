from Handlers.handler import Handler
from View import View


class IndexPageHandler(Handler):
    def perform_get(self) -> None:
        body = View.render("index")
        self.response.body = body




