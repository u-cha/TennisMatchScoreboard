from jinja2 import Environment, PackageLoader, select_autoescape
from View.gamescoretranslator import GameScoreTranslator


class View:
    templates = {
        "index": "index.html",
        "new_match": "new_match.html",
        "match_score": "match_score.html",
        "finished_matches": "finished_matches.html",
        "busy_player": "player_is_busy.html",
        "match_not_found": "match_not_found.html"
    }

    env = Environment(
        loader=PackageLoader("View", package_path="templates"),
        autoescape=select_autoescape()
    )

    @classmethod
    def __get_template_by_name(cls, name):
        template = cls.env.get_template(cls.templates.get(name))

        return template

    @classmethod
    def render(cls, name, *args, **kwargs):
        template = cls.__get_template_by_name(name)
        if kwargs.get("current_game"):
            kwargs["current_game"] = GameScoreTranslator.translate(kwargs["current_game"])
        return template.render(*args, **kwargs)
