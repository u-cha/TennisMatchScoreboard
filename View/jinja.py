from jinja2 import Environment, PackageLoader, select_autoescape


class View:
    templates = {
        "index": "index.html",
        "new_match": "new_match.html",
        "match_score": "match_score.html",
        "matches": "matches.html"
    }

    env = Environment(
        loader=PackageLoader("View"),
        autoescape=select_autoescape()
    )

    @classmethod
    def __get_template_by_name(cls, name):
        template = cls.env.get_template(cls.templates.get(name))
        return template

    @classmethod
    def render(cls, name, *args, **kwargs):
        template = cls.__get_template_by_name(name)
        return template.render(*args, **kwargs)
