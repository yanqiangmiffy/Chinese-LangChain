from __future__ import annotations

from typing import List, Tuple

from app_modules.utils import *


def postprocess(
        self, y: List[Tuple[str | None, str | None]]
) -> List[Tuple[str | None, str | None]]:
    """
    Parameters:
        y: List of tuples representing the message and response pairs. Each message and response should be a string, which may be in Markdown format.
    Returns:
        List of tuples representing the message and response. Each message and response will be a string of HTML.
    """
    if y is None or y == []:
        return []
    temp = []
    for x in y:
        user, bot = x
        if not detect_converted_mark(user):
            user = convert_asis(user)
        if not detect_converted_mark(bot):
            bot = convert_mdtext(bot)
        temp.append((user, bot))
    return temp


with open("./assets/custom.js", "r", encoding="utf-8") as f, open("./assets/Kelpy-Codos.js", "r",
                                                                  encoding="utf-8") as f2:
    customJS = f.read()
    kelpyCodos = f2.read()


def reload_javascript():
    print("Reloading javascript...")
    js = f'<script>{customJS}</script><script>{kelpyCodos}</script>'

    def template_response(*args, **kwargs):
        res = GradioTemplateResponseOriginal(*args, **kwargs)
        res.body = res.body.replace(b'</html>', f'{js}</html>'.encode("utf8"))
        res.init_headers()
        return res

    gr.routes.templates.TemplateResponse = template_response


GradioTemplateResponseOriginal = gr.routes.templates.TemplateResponse
