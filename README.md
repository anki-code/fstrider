**Strider** is a file system navigator:
* to reduce keystrokes during navigation.
* to remember and reuse the behavior and choices.
* to be minimalistic until it's needed to do more.
* to create new paths without annoying asking.


## Install

Before installation read the text below about using `/` when copying or moving files and directories.

Install or update:

```xsh
pip install -U git+https://github.com/anki-code/strider
```

## Usage
Run strider and start striding:
```xsh
strider
```

In the xonsh shell you can load xontrib with `s` alias that works fast and allows to change directory using strider:
```xsh
xontrib load strider
s
```

### Keys

Basic:

* <kbd>Left</kbd> - move to parent directory.
* <kbd>Right</kbd> - move to the selected directory.
* <kbd>Space</kbd> - open menu for the current file or directory.
* <kbd>Enter</kbd> - open file or directory using OS associations.
* <kbd>Esc</kbd> - quit.

Additional:

* <kbd>Shift ~</kbd> - jump to the home directoy.
* <kbd>Control j</kbd> - jump to path. You can jump into new path and then create it.
* <kbd>Control d</kbd> - jump to directory from history.
* <kbd>Control +</kbd> - copy path to the current directory.

Midnight Commander bindings:

* <kbd>F5</kbd> - copy.
* <kbd>F6</kbd> - move.
* <kbd>F7</kbd> - rename.
* <kbd>F8</kbd> - delete.
* <kbd>F10</kbd> - quit.
* <kbd>F12</kbd> - open with.

### Using `/` when copying or moving.

Strider was created to reduce keystrokes. So remember two things:
* Any new path will be created automatically. When you copy the file `example.txt` to `/tmp/some/new/path/` the path `/tmp/some/new/path/` will be created automatically.
* If you copy directory `/tmp/dir1` and the target path ends with `/` e.g. `/tmp/other/` then the `dir1` will be putted into `/tmp/other/dir`.
* If you copy directory `/tmp/dir2` and the target path ends with directory name e.g. `/tmp/other` then the `dir2` will be merged with `/tmp/other`. Existing files will be overwritten.

## Good to know

* Copy the current path in MacOS Finder: <kbd>Option Command C</kbd>
* Jump to path in MacOS Finder: <kbd>Command Shift G</kbd>

## Known issues

### Tested only on Mac OS

Current version of strider is using and testing on Mac OS. It will be good to test and fix for Linux and Windows.

## Future features

Feel free to grab and implement. PR is welcome!

### Shell integration
#### Xonsh shell
- Using xonsh shell history to jump into directories.
- Run shell command in this directory.
#### Other shells support.
- Change current directory.
### Navigation
- Up key at first option moves cursor to end.
### Dialog
- Put cursor to the end of line
- Enter-Esc alternative to Ok/Cancel buttons.
- Autocomplete for paths in menu - the feature from prompt-toolkit.
  - Use path from clipboard.
- Copying progress bar or just the console log from `rsync`.
### List
- Modes: short, full.
  - Show file chmod/chown in title.
- Sorting by size `sorted(glob.glob('*.png'), key=os.path.getsize)`.
- Draggable items. `ls --hyperlink`
- Fuzzy search.
### Integration
- "=" to move object from path to the current dir.
### App association
- `.xonshrc` case in app_assoc.
- Highlight known suffix from app_assoc.
- Using $LS_COLORS and `dircolors` for color files.
### Title
- Show what part of path is exist and what new.
- Show chown/chmod if "Access denied".
### Env options
- The way to switch on/off env options.
- Way to change key bindings.
### Style
- Dark style.
### Debug
- Debug mode
- Show errors like in case of exception.
### Tech
- Resolve '/tmp/../../'
- Symlinks: copying, moving

## Ideas

Just ideas for future features.

### List
#### Fake files (items in the list)
- Fake deleted file to show that this file was deleted.
- Interstellar wormhole - path to another path added to this directory.
  - Read the path from files in this directory.
- Gradient: by time, by size. Show old files with dark color. Show small files with dark color.
### Integration
- Catching pasting path from clipboard and ask actions: cd-ing, copy/move from, open.
- [Async update the list](https://github.com/anki-code/strider/issues/1)
- Using strider for anything e.g. striding around aws s3 bucket, ssh host.
  - The way to setup strider for special needs: colors, menus, hotkeys.
### Keys
- Free keys to use: `/`, `-`.
- VI-mode: bind keys like in vim.
### AI
- Predict the next choice of path based on history and maybe files in dir.
