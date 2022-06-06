# - Project: HTML Editor
# - File   : keywords.py
# - Author : Laurens Nolting

""" REFERENCE: https://developer.mozilla.org/en-US/docs/Web/HTML/Element """

HTML_KEYWORDS = [# - MAIN ROOT - #
                 "html",

                 # - DOCUMENT METADATA - #
                 "head", "link", "meta", "style", "title",

                 # - SECTIONING ROOT - #
                 "body",

                 # - CONTENT SECTIONING - #
                 "address", "article", "aside", "footer", "header", "h1", "h2", "h3", "h4", "h5", "h6",
                 "hgroup", "nav", "section",

                 # - TEXT CONTENT - #
                 "blockquote", "dd", "dir", "div", "dl", "dt", "figcaption", "figure", "hr", "li",
                 "main", "ol", "p", "pre", "ul",

                 # - IMAGE AND MULTIMEDIA - #
                 "area", "audio", "img", "map", "track", "video",

                 # - EMBEDDED CONTENT - #
                 "applet", "embed", "iframe", "noembed", "object", "param", "picture", "source",

                 # - SCRIPTING - #
                 "canvas", "noscript", "script",

                 # - DEMARCATING EDITS - #
                 "del", "ins",

                 # - TABLE CONTENT - #
                 "caption", "col", "colgroup", "table", "tbody", "td", "tfoot", "th", "thead", "tr",

                 # - FORMS - #
                 "button", "datalist", "fieldset", "form", "input", "label", "legend", "meter",
                 "optgroup", "option", "output", "progress", "select", "textarena",

                 # - INTERACTIVE ELEMENTS - #
                 "details", "dialog", "menu", "menuitem", "summary",

                 # - WEB COMPONENTS - #
                 "content", "element", "shadow", "slot", "template"
                ]

HTML_INLINE_KEYWORDS = [# - INLINE TEXT SEMANTICS - #
                        "a", "abbr", "b", "bdi", "bdo", "br", "cite", "code", "data",
                        "dfn", "em", "i", "kbd", "mark", "q", "rp", "rt", "rtc", "ruby",
                        "s", "samp", "small", "span", "strong", "sub", "sup", "time",
                        "tt", "u", "var", "wbr"]

HTML_KEYWORDS_ALL = HTML_KEYWORDS + HTML_INLINE_KEYWORDS
