# denite-anzu
denite.nvim source for vim-anzu

## Installation
Put this repo in your &rtp or install by your favorite vim plugin manager such as [Shougo/dein.vim](http://github.com/Shougo/dein.vim)

### Requirement
Currently this plagin doesn't work in Neovim.
- [Shougo/denite.nvim](http://github.com/Shougo/denite.nvim)
- [osyo-manga/vim-anzu](http://github.com/osyo-manga/vim-anzu)

## Usage
:Denite anzu[:{pattern}]

## Example

```
"in .vimrc
nnoremap <silent> <Leader>/ :<C-u>Denite
    \ -mode=normal
    \ -auto-action='highlight'
    \ anzu<CR>
```

