let s:path = fnamemodify(resolve(expand('<sfile>:p')), ':h') . "/sourcegraph_vi.py"

if !has('python')
	finish
endif

if !exists("g:SOURCEGRAPH_AUTO") || g:SOURCEGRAPH_AUTO == "true"
    augroup SourcegraphVim
        autocmd VimEnter     * call LookupSymbol()
        autocmd VimLeavePre  * call LookupSymbol()
        autocmd CursorMoved  * call LookupSymbol()
        autocmd CursorMovedI * call LookupSymbol()
        autocmd BufEnter     * call LookupSymbol()
        autocmd BufLeave     * call LookupSymbol()
    augroup END
endif

let s:last_filename = ''
let s:last_word = ''
let s:last_word_small = ''
let s:last_offset = 0
let s:last_linenumber = -1

au BufNewFile,BufRead *.go set filetype=go

function! LookupSymbol()
	let s:is_dirty = &modified
	let s:filename = expand('%:p')
	let s:selected_token = expand('<cWORD>')
	let s:currword_small = expand('<cword>')
	let s:cursor_offset = line2byte(line(".")) + col(".") - 1
	let s:numlines = line('$')
	let s:linenumber = line('.')
	if s:filename == s:last_filename && s:currword_small == s:last_word_small && s:linenumber == s:last_linenumber
	else
		let s:last_filename = s:filename
		let s:last_word = s:selected_token
		let s:last_word_small = s:currword_small
		let s:last_offset = s:cursor_offset
		let s:last_linenumber = s:linenumber
    execute "pyfile " . s:path
	endif
endfunction

command! GRAPH call LookupSymbol()
