
# -*- coding: utf-8 -*-

from .base import Base
from typing import List, Dict, Union
from denite.util import abspath, Nvim, UserContext, Candidates


HIGHLIGHT_SYNTAX: List[Dict[str, Union[str, bool]]] = [
    {"name": "Prefix", "link": "Constant", "re": r"\v\d+\s[\ ahu%#+]+"},
    {"name": "Info", "link": "PreProc", "re": r"\v\[[^]]*\]"},
    {"name": "Modified", "link": "Statement", "re": "+", "in": "Prefix"},
    {"name": "Time", "link": "Statement", "re": r"\v\([^)]*\)"},
    {"name": "File", "link": "Function", "re": r"\v[^/ [\]]+\ze\s(\[|\()"},
    {"name": "File", "link": "Function", "re": r"\v[^/ [\]]+\ze\n"},
    {"name": "Special", "link": "Special", "re": r"\v\$[A-Z]+"},
    {"name": "Icon", "link": "String", "re": r"\].\["},
    {"name": "IconConceal", "is_conceal": True, "in": "Icon", "re": r"[[\]]"},
]


def highlight(vim: Nvim, syntax_name: str) -> None:
    for syn in HIGHLIGHT_SYNTAX:
        conceal = "conceal " if syn.get("is_conceal") else ""
        containedin = syntax_name + ("_" + str(syn["in"]) if "in" in syn else "")
        vim.command(
            "syntax match {0}_{1} /{2}/ {3}contained containedin={4}".format(
                syntax_name, syn["name"], syn["re"], conceal, containedin
            )
        )
        if not syn.get("is_conceal"):
            vim.command(
                "highlight default link {0}_{1} {2}".format(
                    syntax_name, syn["name"], syn["link"]
                )
            )


class Source(Base):

    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)
        self.name = 'anzu'
        self.kind = 'file'
        self.sorters = []
        self.matcher = []

    def on_init(self, context: UserContext) -> Candidates:
        context['__bufnr'] = str(self.vim.current.buffer.number)

    def gather_candidates(self, context: UserContext) -> None:
        candidates: Candidates = []
        # status = self.vim.call('anzu#search_status')
        args = []
        if len(context['args']) >= 1:
            args = context['args'][0]
        else:
            args = ''
        bufnr = context['__bufnr']
        loclist = self.vim.call('anzu#searchpos', args, bufnr, 2)
        start = 0
        for loc in loclist:
            if start == loc[0]:
                pass
            else:
                start = loc[0]
                lines = self.vim.call('getbufline', '%', loc[0])
                abbr = '[%d:%d] %s' % (loc[0], loc[1], lines[0])
                line = [{
                        'word': lines[0],
                        'abbr': abbr,
                        'action__bufnr': bufnr,
                        'action__path':
                            abspath(self.vim, self.vim.current.buffer.name),
                        'action__line': loc[0],
                        'action__col': loc[1],
                        'action__pattern': args
                        }]
                candidates += line
        return candidates

    def highlight(self) -> None:
        highlight(self.vim, self.syntax_name)
