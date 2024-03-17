**Strider** is a file system navigator:
* to reduce keystrokes during navigation.
* to remember and reuse the behavior and choices.
* to be minimalistic until it's needed to do more.
* to create new paths without annoying asking.


## Install

**Note! Project status: proof of concept, no guarantees.**

```xsh
pip install git+https://github.com/anki-code/strider
```

## Usage
Run strider and start striding:
```xsh
strider
```

In xonsh shell you can load xontrib with `s` alias that allows to change directory using strider:
```xsh
xontrib load strider
s
```

### Keys

Basic:

* <kbd>←</kbd> = `cd ..` 
* <kbd>→</kbd> = `cd <dir>`
* <kbd>Space</kbd> - open menu.
* <kbd>Enter</kbd> - open file or directory using OS associations.

Additional:

* <kbd>Shift ~</kbd> - jump to the home directoy.
* <kbd>Control J</kbd> - jump to path.
* <kbd>Control +</kbd> - copy path to the current directory.

## Known issues

### Tested only on Mac OS

Current version of strider is using and testing on Mac OS. It will be good to test and fix for Linux and Windows.

