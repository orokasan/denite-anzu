
# -*- coding: utf-8 -*-

from .base import Base
from denite.util import abspath

ANZU_NUMBER_SYNTAX = (
    'syntax match deniteSource_lineNumber '
    r'/\d\+\(:\d\+\)\?/ '
    'contained containedin=')
ANZU_NUMBER_HIGHLIGHT = 'highlight default link deniteSource_lineNumber LineNR'

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'anzu'
        self.kind = 'file'
        self.sorters = []
        self.matcher = []

    def on_init(self, context):
        context['__bufnr'] =  str(self.vim.call('bufnr', '%'))

    def gather_candidates(self, context):
        args = []
        if context['args']:
            args = context['args'][0]
        bufnr = context['__bufnr']
        loclist = self.vim.call('anzu#searchpos',args, bufnr )
        return [self._convert(loc, bufnr, args) for loc in loclist]

    def highlight(self):
        self.vim.command(ANZU_NUMBER_SYNTAX + self.syntax_name)
        self.vim.command(ANZU_NUMBER_HIGHLIGHT)

    def _convert(self, info, buf,args):
        lines = self.vim.call('getbufline','%', info[0] )
        abbr = '[%d:%d] %s' % (info[0], info[1], lines[0])
        return {
                'word': lines[0],
                'abbr': abbr,
                'action__bufnr': buf,
                'action__path':abspath(self.vim, self.vim.current.buffer.name),
                'action__line': info[0],
                'action__col': info[1],
                'action__pattern': args
                }
