set nocompatible              " be iMproved
filetype off                  " required!

set rtp+=~/.vim/bundle/vundle/
call vundle#rc()

Bundle 'gmarik/vundle'
Bundle 'tpope/vim-fugitive'
Bundle 'Lokaltog/vim-easymotion'
Bundle 'rstacruz/sparkup', {'rtp': 'vim/'}
Bundle 'L9'
Bundle 'FuzzyFinder'
Bundle 'git://git.wincent.com/command-t.git'
Bundle 'Syntastic'
Bundle 'altercation/vim-colors-solarized'
Bundle 'tpope/vim-surround'
Bundle 'vim-scripts/pep8'
Bundle 'vim-scripts/The-NERD-tree'

" see :h vundle for more details or wiki for FAQ
" NOTE: comments after Bundle commands are not allowed.

filetype plugin indent on     " required!

syntax enable
set background=dark
colorscheme solarized
