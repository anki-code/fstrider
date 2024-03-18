**Strider** is a file system navigator:
* to reduce keystrokes during navigation.
* to remember and reuse the behavior and choices.
* to be minimalistic until it's needed to do more.
* to create new paths without annoying asking.


## Install

**Note before installation!**
* Project status: proof of concept. No guarantees, use it carefully until you get 1.0.0 version.
* Read the text below about using `/` when copying or moving.

```xsh
pip install git+https://github.com/anki-code/strider
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

* <kbd>←</kbd> - `cd ..` .
* <kbd>→</kbd> - `cd <dir>`.
* <kbd>Space</kbd> - open menu.
* <kbd>Enter</kbd> - open file or directory using OS associations.
* <kbd>Esc</kbd> - quit.

Additional:

* <kbd>Shift ~</kbd> - jump to the home directoy.
* <kbd>Control j</kbd> - jump to path. You can jump into new path and then create it.
* <kbd>Control d</kbd> - jump to directory from history.
* <kbd>Control +</kbd> - copy path to the current directory.

### Using `/` when copying or moving.

Strider was created to reduce keystrokes. So remember two things:
* Any new path will be created automatically. When you copy the file `example.txt` to `/tmp/some/new/path/` the path `/tmp/some/new/path/` will be created automatically.
* If you copy directory `/tmp/dir1` and the target path ends with `/` e.g. `/tmp/other/` then the `dir1` will be putted into `/tmp/other/dir`.
* If you copy directory `/tmp/dir2` and the target path ends with directory name e.g. `/tmp/other` then the `dir2` will be merged with `/tmp/other`. Existing files will be overwritten.

## Known issues

### Tested only on Mac OS

Current version of strider is using and testing on Mac OS. It will be good to test and fix for Linux and Windows.

