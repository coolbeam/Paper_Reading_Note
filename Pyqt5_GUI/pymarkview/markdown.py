import html
import re
from collections import OrderedDict
from typing import Union, Callable


class Markdown:
    class RuleSetContainer:
        def __init__(self):
            self._rules = OrderedDict()

        def __call__(self):
            return self._rules.items()

        def add_rule(self, rule: str, repl: Union[str, Callable[[str], str]]):
            # print(type(repl))
            key = re.compile(rule)
            self._rules[key] = repl

    def __init__(self):
        self.rules_cont = Markdown.RuleSetContainer()
        self.rules_cont.add_rule(r"(?m)^ {0,3}(#+)\s(.*)", self._html_header)
        self.rules_cont.add_rule(r"([^\n]+)\n(\={3,}|\-{3,})", self._html_header_alt)
        self.rules_cont.add_rule(r"\n\s{0,3}(\*{3,}|\_{3,}|\-{3,})\n", "<hr>")
        self.rules_cont.add_rule(r"\[\!\[(.*?)\]\((.*?)\)\]\((.*?)\)", r"<a href='\3'><img src='\2' alt='\1'/></a>")
        self.rules_cont.add_rule(r"\!\[([^\[]+)\]\(([^\)]+)\)", r"<img src='\2' alt='\1'>")
        self.rules_cont.add_rule(r"\[([^\[]+)\]\(([^\)]+)\)", r"<a href='\2'>\1</a>")
        self.rules_cont.add_rule(r"(\*\*|__)(.*?)\1", r"<strong>\2</strong>")
        self.rules_cont.add_rule(r"(\*|_)(.*?)\1", r"<em>\2</em>")
        self.rules_cont.add_rule(r"(\~\~)(.*?)\1", r"<del>\2</del>")
        self.rules_cont.add_rule(r"(?s)\n`{3}([\S]+)?\n(.*?)\n`{3}", self._html_pre)
        # self.rules_cont.add_rule(r"(?m)^((?:(?:[ ]{4}|\t).*(\n|$))+)", r"<pre>\1</pre>")
        self.rules_cont.add_rule(r"\`(.*?)\`", self._html_code)
        self.rules_cont.add_rule(r"(?sm)(^(?:[*+-]|\d+\.)\s(.*?)(?:\n{2,}))", self._html_list)
        self.rules_cont.add_rule(r"(?s)\n\>\s(.*?)(?:$|\n{2,})", self._html_blockquote)
        self.rules_cont.add_rule(r"\<(http.*?)\>", r"<a href='\1'>\1</a>")
        self.rules_cont.add_rule(r"\[\[(.*?)\]\]", r"<a href='pmv://\1'>📁\1</a>")
        self.rules_cont.add_rule(r"(?s)(.*?[^\:\-\,])(?:$|\n{2,})", self._html_parag)

    def parse(self, text: str) -> str:
        text = "\n{}\n\n".format(text)

        for rule, repl in self.rules_cont():
            text = re.sub(rule, repl, text)

        return text

    def _html_header(self, match_obj) -> str:
        level = min(match_obj.group(1).count('#'), 6)
        text = match_obj.group(2)
        return "<h{level}>{text}</h{level}>".format(level=level, text=text)

    def _html_header_alt(self, match_obj) -> str:
        level = 1 if match_obj.group(2)[0] == "=" else 2
        text = match_obj.group(1)
        return "<h{level} class='alt'>{text}</h{level}>".format(level=level, text=text)

    def _html_code(self, match_obj) -> str:
        text = html.escape(match_obj.group(1))

        return "<code>{text}</code>".format(text=text)

    def _html_pre(self, match_obj) -> str:
        lang = match_obj.group(1)
        text = html.escape(match_obj.group(2))

        return "<pre lang='{lang}'>{text}</pre>".format(lang=lang, text=text)

    def _html_list(self, match_obj) -> str:
        def outer_tags(ch: str):
            return ("<ol>", "</ol>") if ch.isdigit() else ("<ul>", "</ul>")

        lines = (match_obj.group(1)[0] + " " + match_obj.group(2)).split("\n")

        virt_list = {}

        for number, line in enumerate(lines):
            level = (len(line) - len(line.lstrip())) // 2
            text = line.strip().partition(" ")[2]
            virt_list.update(
                {
                    number: {
                        "level": level,
                        "text": text,
                        "type": (line.lstrip() + "*")[0]
                    }
                }
            )

        res = outer_tags(match_obj.group(1)[0])[0]

        for number in range(len(lines)):
            current = virt_list.get(number)
            successor = virt_list.get(number + 1, None)

            res += "<li>{text}</li>".format(text=current["text"])

            if successor:
                level_delta = successor["level"] - current["level"]

                if level_delta > 0:
                    res += outer_tags(successor["type"])[0]
                elif level_delta < 0:
                    res += outer_tags(current["type"])[1] * abs(level_delta)

            if not successor and current["level"] > 0:
                res += outer_tags(current["type"])[1]

        res += outer_tags(match_obj.group(1)[0])[1]

        return res

    def _html_parag(self, match_obj) -> str:
        text = match_obj.group(1)

        starts_with_tag = re.compile(r"^<\/?(li|h|p|block|img|hr|ul|ol|pre)")

        if starts_with_tag.match(text):
            return "\n{text}\n".format(text=text)
        else:
            return "\n<p>{text}</p>\n".format(text=text)

    def _html_blockquote(self, match_obj) -> str:
        text = match_obj.group(1).replace(">", "<br>")

        return "\n<blockquote>{text}</blockquote>".format(text=text)
