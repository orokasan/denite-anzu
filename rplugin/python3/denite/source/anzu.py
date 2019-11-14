
# -*- coding: utf-8 -*-

from .base import Base
from denite.util import abspath, Nvim, UserContext, Candidates
#ANZU_NUMBER_SYNTAX = (
#    'syntax match deniteSource_lineNumber '
#    r'/\d\+\(:\d\+\)\?/ '
#    'contained containedin=')
#ANZU_NUMBER_HIGHLIGHT = 'highlight default link deniteSource_lineNumber LineNR'

class Source(Base):

    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)
        self.name = 'anzu'
        self.kind = 'file'
        self.sorters = []
        self.matcher = []

    def on_init(self, context: UserContext) -> Candidates :
        context['__bufnr'] = str(self.vim.current.buffer.number)

    def gather_candidates(self, context: UserContext) -> None:
        candidates: Candidates = []
        status = self.vim.call('anzu#search_status')
        args = []
        if len(context['args']) >= 1 :
            args = context['args'][0]
        else: 
            args = ''
        bufnr = context['__bufnr']
        loclist = self.vim.call('anzu#searchpos', args, 0)
        for loc in loclist:
            lines = self.vim.call('getbufline','%', loc[0] )
            abbr = '[%d:%d] %s' % (loc[0], loc[1], lines[0])
            line =  [{
                    'word': lines[0],
                    'abbr': abbr,
                    'action__bufnr': bufnr,
                    'action__path':abspath(self.vim, self.vim.current.buffer.name),
                    'action__line': loc[0],
                    'action__col': loc[1],
                    'action__pattern': args
                    }]
            candidates += line
        return candidates

#    def highlight(self):
#        self.vim.command(ANZU_NUMBER_SYNTAX + self.syntax_name)
#        self.vim.command(ANZU_NUMBER_HIGHLIGHT)
