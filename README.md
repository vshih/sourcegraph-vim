# Sourcegraph for Vim [![CircleCI](https://circleci.com/gh/sourcegraph/sourcegraph-sublime.svg?style=svg)](https://circleci.com/gh/sourcegraph/sourcegraph-sublime)

*Sourcegraph for Vim is in beta mode. Feedback or issue? Please email us at support@sourcegraph.com or [file an issue.](https://github.com/sourcegraph/sourcegraph-vim/issues)*

## Overview

Sourcegraph for Vim allows you to view Go definitions on [sourcegraph.com](http://www.sourcegraph.com) as you code, so you can stay focused on what's important: your code. When your cursor is on a Go symbol and you run :GRAPH (or a remapped hotkey), it should load in a channel in your browser:

## Setup

To install Sourcegraph for Vim, follow the instructions for your Vim package manager.

* [Pathogen](https://github.com/tpope/vim-pathogen)
```shell
git clone https://github.com/sourcegraph/sourcegraph-vim.git ~/.vim/bundle/sourcegraph-vim
```

* [Vundle](https://github.com/tpope/vim-pathogen)
```shell
echo "Plugin 'sourcegraph/sourcegraph-vim'" >> ~/.vimrc
vim +PluginInstall +qall
```

* [NeoBundle](https://github.com/Shougo/neobundle.vim)
```shell
echo "NeoBundle 'sourcegraph/sourcegraph-vim'" >> ~/.vimrc
vim +NeoBundleInstall +qall
```

* [vim-plug](https://github.com/junegunn/vim-plug)
```shell
echo "Plug 'sourcegraph/sourcegraph-vim', {'for': ['go']}" >> ~/.vimrc
vim +PlugInstall
```

### .vimrc
Sourcegraph automatically opens a live channel and shows references for your Go code as you type by default. If you want to disable this feature, set the `g:SOURCEGRAPH_AUTO` flag to "false" in your .vimrc file.
```
let g:SOURCEGRAPH_AUTO = "false"
```

![Sourcegraph for Vim](images/setup.jpg)

## Privacy

Sourcegraph for your editor determines the type information for symbols locally on your development machine, using a linter called [godefinfo](https://github.com/sqs/godefinfo). [Check out the communication struct](https://sourcegraph.com/sourcegraph/sourcegraph@fa8331a827a3de3cd02e9e0c687387081dd8f540/-/blob/api/sourcegraph/sourcegraph.proto#L2216) to see what the Sourcegraph editor plugin sends to the Sourcegraph API. If you’d like Sourcegraph for your editor to display usage examples for your private code, [create an account and choose to link your private GitHub repositories at Sourcegraph.com.](https://sourcegraph.com/)

## Usage

Sourcegraph for Vim opens a channel in your browser to initialize your Sourcegraph session when in Go files. As you navigate through Go files, enter the Vim command ```:GRAPH``` when your cursor is on a symbol to load its definition and references across thousands of public Go repositories.

## Map a Vim hotkey

To map Sourcegraph for Vim to a hotkey, add a remap command to your ~/.vimrc file. For instance, to map F2 to :GRAPH, add the following to ~/.vimrc.
```
nnoremap <F2> :GRAPH<CR>
```

## Flags

Sourcegraph for Vim has a number of flags to customize your experience. To change your Sourcegraph settings, open add the following settings to your ~/.vimrc file.

### GOBIN and GOPATH

To learn more about setting your `GOPATH`, please click [here](https://golang.org/doc/code.html#GOPATH).

Sourcegraph for Vim searches your shell to find `GOBIN`, the full path of your Go executable. This is typically `$GOROOT/bin/go`. Similarly, Sourcegraph loads your `/bin/bash` startup scripts to search for the `GOPATH` environment variable. If Sourcegraph cannot find your environment variables, or if you would like to use a custom `GOPATH` or `GOBIN`, add them in the ~/.vimrc file as follows:

```
g:SOURCEGRAPH_GOPATH = "/path/to/gopath"
g:SOURCEGRAPH_GOBIN = "/path/to/gobin"
```

### Logging

To see verbose out put from Sourcegraph for Vim, you can check the contents of the logging file. This logging file can be set in .vimrc, but by default, it is here:
```
g:SOURCEGRAPH_LOG_FILE = "/tmp/sourcegraph-vim.log"
```

## Godefinfo

Sourcegraph for Vim should automatically install `godefinfo` when it loads your settings. If you still receive an error message about `godefinfo` installation, you can install it manually by running the following command:

```shell
go get -u github.com/sqs/godefinfo
```

### Local server

If you want to try Sourcegraph for Vim on a local Sourcegraph server, you can define its base URL in this file using the key `SOURCEGRAPH_BASE_URL` in the ~/.vimrc file.

```
g:SOURCEGRAPH_BASE_URL = "https://sourcegraph.com"
g:SOURCEGRAPH_SEND_URL = "https://grpc.sourcegraph.com"
```

## Diagnostic

Sourcegraph for Vim comes with a diagnostic file called `diagnostic.py`. In case of issues setting up Sourcegraph for Vim, trying running this file to determine the cause. If there is an error that you are unable to debug, please report the output of this tool in issues on GitHub. Here is a sample successful output:
```
python diagnostic.py [-g /path/to/gopath] [-b /path/to/go/binary]
-------------------------
----Printing settings object with default values.
{"SG_CHANNEL": "username-b97d52e5cb54c7f93def242612a934b72d3a", "GOPATH": "/Users/username/gopath", "SG_BASE_URL": "https://sourcegraph.com", "GOBIN": "/usr/local/go/bin/go", "EditorType": "undefined", "SG_SEND_URL": "https://grpc.sourcegraph.com", "VersionMinor": 1, "PATH": "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/go/bin:/Users/username/gopath/bin", "ENABLE_LOOKBACK": true}
----VERIFY GOPATH and PATH settings, to ensure that the go binary is in the PATH, and GOPATH is correctly set.
----Validating settings object. If value is not none, Sourcegraph for your editor is not configured properly.
--------Checking if shell is supported.
--------Checking if `pwd` works on the shell.
--------Checking GOPATH settings.
--------Running go binary and checking version.
--------Checking if godefinfo binary is in $GOPATH/bin, and running godefinfo -v.
----VERIFY output of validate settings is None: None
----Assembling Sourcegraph object.
----VERIFY that $GOPATH/bin is in the path. PATH = /usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/go/bin:/Users/username/gopath/bin
----Testing browser settings.
----VERIFY browser opens.
-------------------------
Diagnostic completed.
-------------------------
```

## Support

Sourcegraph for Vim has been tested on Vim 7.3, and requires Python 2.X or Python 3.X to be compiled with your Vim installation. To determine if your Vim is compiled with Python, try running ```:echo has ('python')``` OR ```:echo has('python3')``` from within Vim, and verify that it does not throw an error.
