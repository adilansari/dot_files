set nocompatible              " be iMproved
filetype off                  " required!

set rtp+=~/.vim/bundle/Vundle.vim/
call vundle#begin()

Plugin 'VundleVim/Vundle.vim'
Plugin 'Lokaltog/vim-easymotion'
Plugin 'L9'
Plugin 'FuzzyFinder'
Plugin 'kien/ctrlp.vim'
Plugin 'wincent/command-t'
Plugin 'Syntastic'
Plugin 'altercation/vim-colors-solarized'
Plugin 'tpope/vim-surround'
Plugin 'scrooloose/nerdtree'
Plugin 'scrooloose/nerdcommenter'
Plugin 'Shougo/neocomplete'
Plugin 'nvie/vim-flake8'
Plugin 'plasticboy/vim-markdown'
Plugin 'Raimondi/delimitMate'
Plugin 'bling/vim-airline'
Plugin 'airblade/vim-gitgutter'
Plugin 'majutsushi/tagbar.git'
Plugin 'luochen1990/rainbow'
Plugin 'derekwyatt/vim-scala'
Plugin 'othree/html5.vim'
Plugin 'pangloss/vim-javascript'

call vundle#end()

" see :h vundle for more details or wiki for FAQ
" NOTE: comments after Plugin commands are not allowed.

filetype plugin indent on     " required!
filetype plugin on
filetype on
"======Solarized theme============
syntax on
let g:solarized_termtrans = 1
set background=dark
"set t_Co=256
let g:solarized_termcolors=256
colorscheme solarized


" ===========sontek.net============
set autoindent    " always set autoindenting on
set backspace=indent,eol,start 		" allow backspacing over everything in insert mode
set copyindent    " copy the previous indentation on
set cursorline
set cursorcolumn
set foldlevel=99    "folding"
set foldmethod=indent
set hidden
set history=1000         " remember more commands and search history
set hlsearch      "
set ignorecase    " ignore case when searching
set incsearch     "
set laststatus=2
set noerrorbells         " don't beep
set nowrap        " don't wrap lines
set number        " always show line numbers
set re=0		" to speed up typescript syntax highlighting
set ruler
set shiftwidth=4  " number of spaces to use for
set shiftround    " use multiple of shiftwidth when indenting with '<' and '>'
set showcmd
set showmatch     " set show matching parenthesis
set smartcase     " ignore case if search pattern is all lowercase,
set smarttab      " insert tabs on the
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*
set tabstop=4     " a tab is four spaces
set showtabline=2
set title                " change the terminal's title
set ttyfast
set undolevels=1000      " use many muchos levels of undo
set visualbell           " don't beep
set wildignore=*.swp,*.bak,*.pyc,*.class

let g:syntastic_auto_loc_list=1
let g:syntastic_loc_list_height=5
let g:syntastic_mode_map = { 'mode': 'passive', 'active_filetypes': [],'passive_filetypes': [] }
let g:airline#extensions#tabline#enabled = 1
let g:jedi#popup_select_first = 0
let g:jedi#auto_vim_configuration = 1
let g:neocomplete#enable_at_startup = 1
let g:neocomplete#enable_smart_case = 1
let g:vim_markdown_folding_disabled=1
let g:ackprg = 'ag --nogroup --nocolor --column'
let g:ctrlp_map = '<c-p>'
let g:ctrlp_cmd = 'CtrlP'
let g:rainbow_active = 0
let mapleader=","

autocmd filetype python set expandtab
"autocmd FileType  python setlocal textwidth=79
"autocmd BufWritePost *.py call Flake8()

nnoremap <F6> :SyntasticCheck<CR> :SyntasticToggleMode<CR>
map <C-o> :NERDTreeToggle<CR>
map <C-n> :nohlsearch<CR>
inoremap <leader>w <esc>:w<cr>a
inoremap <leader>q <esc>:q<cr>
inoremap <leader>o <esc>o<cr>i
nnoremap <silent> <leader>b :TagbarToggle<CR>
nnoremap <leader>. :CtrlPTag<cr>
vmap <C-x> :!pbcopy<CR>  
vmap <C-c> :w !pbcopy<CR><CR> 
