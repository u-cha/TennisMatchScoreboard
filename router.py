from Handlers import IndexPageHandler, NewMatchHandler, OngoingMatchHandler, FinishedMatchesHandler


class Router:
    routes = {"/": IndexPageHandler,
              "/new-match": NewMatchHandler,
              "/match-score": OngoingMatchHandler,
              "/matches": FinishedMatchesHandler
              }

    @classmethod
    def get_handler_class_by_path(cls, path):
        handler_class = cls.routes.get(path, IndexPageHandler)
        return handler_class
