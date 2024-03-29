<p align="center">
<b>fstrider</b> is an intuitive and fast file system navigator for terminal.
</p>

<p align="center">  
<img src="https://repository-images.githubusercontent.com/772009748/a54b45b5-0dbc-4eef-81b1-11d618c6f9e1" width="50%">
</p>
<p align="center">  
If you like it click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Nice%20file%20system%20navigator!&url=https://github.com/anki-code/fstrider" target="_blank">tweet</a>.
</p>


**fstrider** is:
* to reduce keystrokes during navigation.
* to remember and reuse the behavior and choices.
* to be minimalistic until it's needed to do more.
* to create new paths without annoying asking.


## Install

Before installation read the text below about using `/` when copying or moving files and directories.

Install or update:

```xsh
pip install fstrider
# OR: pip install -U git+https://github.com/anki-code/fstrider
```

## Usage
Run fstrider and start striding:
```xsh
fstrider
```

In the xonsh shell you can load xontrib with `s` alias that works fast and allows to change directory using fstrider:
```xsh
xontrib load fstrider
fs      # or fstrider
```

### Key bindings

Basic:

* <kbd>Left</kbd> - move to parent directory.
* <kbd>Right</kbd> - move to the selected directory.
* <kbd>Space</kbd> - open menu for the current file or directory.
* <kbd>Enter</kbd> - open file or directory using OS associations.
* <kbd>Esc</kbd> - quit.

Additional:

* <kbd>Shift ~</kbd> - jump to the home directoy.
* <kbd>Control j</kbd> - jump to path. You can jump into new path and then create it.
* <kbd>Control h</kbd> - jump to directory from history.
* <kbd>Control +</kbd> - copy path to the current directory.

Midnight Commander bindings: <kbd>F5</kbd> copy, <kbd>F6</kbd> move, <kbd>F7</kbd> rename, <kbd>F8</kbd> delete, <kbd>F10</kbd> quit, <kbd>F12</kbd> open with.

### Using `/` when copying or moving.

fstrider was created to reduce keystrokes. So remember two things:
* Any new path will be created automatically. When you copy the file `example.txt` to `/tmp/some/new/path/` the path `/tmp/some/new/path/` will be created automatically.
* If you copy directory `/tmp/dir1` and the target path ends with `/` e.g. `/tmp/other/` then the `dir1` will be putted into `/tmp/other/dir`.
* If you copy directory `/tmp/dir2` and the target path ends with directory name e.g. `/tmp/other` then the `dir2` will be merged with `/tmp/other`. Existing files will be overwritten.

## Xonsh xontrib

fstrider xontrib features:
* Creates alias `fs` (or `fstrider` if `fs` exists).
* Run fstrider as fast as possible.
* Keeps history between running fstrider.

Environment variables for fstrider xontrib:
* `$XONTRIB_FSTRIDER_ALIAS` - change the alias name. Recommended `s`.

## Options

* `'show_symlink_paths': True` - show symlinks in the list.
* `'keys_midnight_commander': True` - use Midnight Commander keys.
* `'monitor_state': False` - Async monitoring of the list and update if new files created.
* `'os_path_change': True` - change os path in xonsh shell.
* `'app_associations_save_file': False` - save filename to apps associations.

You can change the option state by setting environment variable e.g. `$FSTRIDER_MONITOR_STATE=True`.

## Known issues

### Tested only on Mac OS

Current version of fstrider is using and testing on Mac OS. It will be good to test and fix for Linux and Windows.

## Roadmap

Feel free to grab and implement or propose new feature. PR is welcome!

### v0.2.0
```
Xonsh xontrib
    ++ Creates alias `fs` (or `fstrider` if `fs` exists). (0.1.18)
    ++ Run fstrider as fast as possible. (0.1.18)
    ++ Keeps history between running fstrider. (0.1.18)

List
    ++ Async monitoring of the list and update if new files created. (0.1.19)
    
Configuration
    ++ Read env from `os.env`. See `fstrider.env`. (0.1.19)

Integration
    "=" to move object from path to the current dir.

Tech
    Errors processing
        Show errors like in case of exception.
        Process `File exists` error.
    ++ Resolve `/tmp/../../`. (0.1.17)
    Symlinks: copying, moving   
    
Style
    Grey style for copy/move and red style for delete dialogue. 
    
Navigation
    ++ Up key at first option moves cursor to end. (0.1.19)
    Fix left key when go from history.    
    Fix right key when go to file from history.
```

### v0.3.0

```
Navigation
    Go back to previous directory after moving or copying.
    
List
    Sorting by size/date `sorted(glob.glob('*.png'), key=os.path.getsize)`.
    Modes: short, full (chmod/chown/date). 

Jump
    Use path from clipboard e.g. `text_area.buffer.paste_clipboard_data`.
    Use directories from xonsh history i.e. `__xonsh__.history[-1].cwd`
```

### v0.4.0
```
Title
    Show chown/chmod if "Access denied".
    Show what part of path is exist and what's new.
    
Dialog
    Autocomplete for paths in menu - the feature from prompt-toolkit.
    Copying progress bar or just the console log from `rsync`.
```

### v0.5.0
```
List
    Fuzzy search.
    Research: Draggable items i.e. `ls --hyperlink`.
    
Associations
    `.xonshrc` case in app_assoc.
    Highlight known suffix from app_assoc.
    Using $LS_COLORS and `dircolors` for color files.    
```

### v0.6.0
```
List
    Improve speed of list on big amount of items - 10k+
```

### Waiting for community

```
Integration
    Other shells support.
    
Key bindings
    The way to change key bindings.
    VI mode, Emacs mode.
    
Style
    Dark style.
```

### Ideas for future
```
List
    Fake files (items in the list)
        Fake deleted file to show that this file was deleted.
        Interstellar wormhole - path to another path added to this directory.
    Read the path from files in this directory.
    Colors and gradient: by time, by size. Show old files with dark color. Show small files with dark color.
    
Integration
    Catching pasting path from clipboard and ask actions: cd-ing, copy/move from, open.
    Using fstrider for anything e.g. striding around aws s3 bucket, ssh host.
        The way to setup fstrider for special needs: colors, menus, hotkeys.
Keys
    Free keys to use: `/`, `-`.
    
Xonsh shell
    Using xonsh shell history to jump into directories.
    Run shell command in this directory.
        Crazy: use xonsh prompt as a prompt for ptk `TextArea`
AI
    Predict the next choice of path based on history and maybe files in dir.
```

## Good to know

* Copy the current path in MacOS Finder: <kbd>Option Command C</kbd>
* Jump to path in MacOS Finder: <kbd>Command Shift G</kbd>
