import json
import os
import pathlib
import shutil
import subprocess
import html
import functools

from xonsh.platform import ON_LINUX, ON_DARWIN

from pathlib import Path
from prompt_toolkit import HTML
from prompt_toolkit.keys import Keys
from prompt_toolkit.styles import Style
from prompt_toolkit.layout import Layout
from prompt_toolkit.application import Application
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.widgets import RadioList, Label, HorizontalLine
from prompt_toolkit.shortcuts import input_dialog, yes_no_dialog, message_dialog
from prompt_toolkit.key_binding.key_bindings import KeyBindings, merge_key_bindings
from prompt_toolkit.layout.containers import FloatContainer

from prompt_toolkit.layout.containers import (
    AnyContainer,
    ConditionalContainer,
    Container,
    Float,
    FloatContainer,
    HSplit,
    Window,

)
from prompt_toolkit.widgets import Shadow, Box

import datetime
from asyncio import Future, ensure_future

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import (
    ConditionalContainer,
    Float,
    HSplit,
    VSplit,
    Window,
    WindowAlign,
)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.lexers import DynamicLexer, PygmentsLexer
from prompt_toolkit.search import start_search
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import (
    Button,
    Dialog,
    Label,
    MenuContainer,
    MenuItem,
    SearchToolbar,
    TextArea,
)

#from .ptk import list_dialog, ChooseList




class TextInputDialog:
    def __init__(self, title="", label_text="", text_area_text='', completer=None):
        self.future = Future()

        def accept_text(buf):
            get_app().layout.focus(ok_button)
            buf.complete_state = None
            return True

        def accept():
            self.future.set_result(self.text_area.text)

        def cancel():
            self.future.set_result(None)

        self.text_area = TextArea(
            completer=completer,
            multiline=False,
            width=D(preferred=40),
            accept_handler=accept_text,
            text=text_area_text
        )

        ok_button = Button(text="OK", handler=accept)
        cancel_button = Button(text="Cancel", handler=cancel)

        self.dialog = Dialog(
            title=title,
            body=HSplit([Label(text=label_text), self.text_area]),
            buttons=[ok_button, cancel_button],
            width=D(preferred=80),
            modal=True,
        )
        # self.dialog = list_dialog('321','123', values=[('1','1'), ('2','2')], is_modal=True)

    def __pt_container__(self):
        return self.dialog


def copy_to_clp(s):
    import pyperclip
    pyperclip.copy(s)

def sort_files(list_sets):
    def sort_func(s):
        return str(s[0]).lower()

    return sorted(list_sets, key=sort_func)

def open_in_os(filename: Path, app_name: str = None):
    if app_name:
        return subprocess.call(('open', '-a', app_name, '-F', filename))
    else:
        return subprocess.call(('open', '-F', filename))

def get_os_applications():
    if ON_DARWIN:
        apps = [a.name.replace('.app', '').replace('.pkg', '') for a in Path('/Applications').glob('*') if
                not str(a.name).startswith('.')]
    else:
        raise Exception('Unsupported platform.')

    apps = sorted(apps, key=lambda s: s.lower())
    return apps

def has_read_access(path):
    return os.access(path, os.R_OK)

def access_type(path):
    p = Path(path)
    p_access = has_read_access(path)
    try:
        p_exists = p.exists()
    except PermissionError:
        p_exists = None

    if p_exists is None:
        return 'noaccess'
    else:
        if p_exists:
            if p_access:
                return 'exist_access'
            else:
                return 'exist_noaccess'
        else:
            return 'notexist'

def get_index_in_values(values, payload=None, text=None, default_index=0):
    for num, p in enumerate(values):
        if payload and (str(p[0]) == payload or p[0] == payload):
            return num
        if text and p[1] == text:
            return num
    return default_index

def create_path_if_needed(path):
    if not (path := Path(path)).exists():
        path.mkdir(parents=True, exist_ok=True)

# def open_in_terminal(filename: Path):
#     subprocess.call(('vim', filename))




class Strider:
    history = {}
    env = {
        'show_symlink_paths': True,
        'app_associations_save_file': False
    }

    def __init__(self, current_path: Path):
        self.title = Label('Welcome to Strider!')

        self.current_path = Path(current_path).absolute()
        self.list = self.create_list()

        self._app_associations_file = '/tmp/strider_app_associations_file.json'
        self.app_associations = self.load_app_associations()

        self.style = self.load_style()

        self.bindings = KeyBindings()


    def __del__(self):
        Path(self._app_associations_file).write_text(json.dumps(self.app_associations))


    def stride(self):
        first_selected = None
        if not self.current_path.is_dir():
            first_selected = self.current_path
            self.history[str(self.current_path.parent)] = str(self.current_path)
            self.current_path = self.current_path.parent
        self.update_list(selected_by_value=first_selected, file_msg={first_selected: "I'm here!"})

        self.root_container = FloatContainer(
            content=HSplit([self.title, self.list]),
            floats=[
                # Float(
                #     xcursor=True,
                #     ycursor=True,
                #     content=ConditionalContainer(
                #         content=Shadow(body=title), filter=True
                #     ),
                # ),
            ]
        )
        layout = Layout(self.root_container)

        application = Application(
            layout=layout,
            key_bindings=merge_key_bindings([load_key_bindings(), self.bindings]),
            mouse_support=True,
            full_screen=True,
            style=self.style,
        )

        application.run()

    def load_style(self):
        style = Style.from_dict({})

        # style = Style.from_dict({
        #     'dialog': 'bg:#111111',
        #     'dialog frame.label': 'bg:#ffffff #000000',
        #     'dialog.body': 'bg:#000000 #111111',
        #     'dialog shadow': 'bg:#111111',
        # })

        # try:
        #     # https://python-prompt-toolkit.readthedocs.io/en/stable/pages/advanced_topics/styling.html
        #     from prompt_toolkit.styles.pygments import style_from_pygments_cls
        #     from pygments.styles import get_style_by_name
        #     style = style_from_pygments_cls(get_style_by_name('monokai'))
        # except:
        #     pass

        return style

    def load_app_associations(self):
        if Path(self._app_associations_file).exists():
            with open(self._app_associations_file, 'r') as f:
                return json.load(f)
        else:
            return {
                '.py': 'PyCharm CE',
                '.txt': 'kate',
            }
                
    def set_title(self, p: Path, msg=None):

        at = access_type(p)
        if 'noaccess' in at:
            color = 'red'
            if not msg:
                msg = 'Access denied'  # FEAT: add chown/chmod
        elif 'notexist' in at:
            color = 'grey'
        else:
            color = 'orange'


        txt = f'<style fg="{color}">' + (html.escape(str(p.parent)) if str(p.parent) != '/' else '') \
                + '/' + f'</style><style fg="{color}"><b>' + html.escape(p.name) + '</b></style>'

        if msg:
            txt += f'<style fg="grey"> - {html.escape(msg)}</style>'

        self.title.text = HTML(txt)


    def create_list(self):
        default = None  # todo
        radio_list = RadioList([('', '')], default)
        radio_list.open_character = radio_list.close_character = ''
        radio_list.control.key_bindings.remove("enter")  # Remove the enter key binding so that we can augment it
        radio_list.control.key_bindings.remove("space")

        @radio_list.control.key_bindings.add("left")
        def _list_left(event):
            self.move(self.current_path.parent)

        @radio_list.control.key_bindings.add("enter")
        def _list_enter(event):
            radio_list._handle_enter()
            selected_item = radio_list.current_value
            if type(selected_item) is pathlib.PosixPath:
                self.move(selected_by_value=radio_list.current_value, file_msg={radio_list.current_value: 'Open with OS'})
                open_in_os(radio_list.current_value)
            elif callable(selected_item):
                selected_item(self.current_path)

        @radio_list.control.key_bindings.add("right")
        def _list_right(event):
            radio_list._handle_enter()
            cv = radio_list.current_value
            if type(cv) is pathlib.PosixPath and cv.is_dir():
                self.move(radio_list.current_value)
            else:
                # open_in_terminal(radio_list.current_value)
                pass

        @radio_list.control.key_bindings.add("space")
        def _list_space(event):
            radio_list._handle_enter()
            if type(radio_list.current_value) is pathlib.PosixPath:
                self.move(radio_list.current_value, title_msg='Actions', update_list=False)
                radio_list.values = self.list_file_actions(radio_list.current_value)
                radio_list._selected_index = 0
                self.history[str(radio_list.current_value.parent)] = str(radio_list.current_value)

        @radio_list.control.key_bindings.add("c-j")
        def _key_jump(event):
            def callback(result_path, input_data):
                if result_path:
                    self.move(Path(result_path).expanduser().absolute())

            self.input_dialog(title='Jump', label_text='Jump to:', callback=callback)

        @radio_list.control.key_bindings.add("~")
        def _key_jump_home(event):
            self.move(Path('~').expanduser())

        @radio_list.control.key_bindings.add("+")
        def _key_copy_from_path(event):
            def callback(source_path: str, input_data: dict):
                r = self.copy(Path(source_path), str(input_data['target_path'])+'/')
                self.move(r['move']['p'], selected_by_value=r['move']['selected_by_value'],
                          file_msg=r['move']['file_msg'])
                return r['result']
            self.input_dialog(title='Copy from', label_text='Copy here this:', callback=callback, input_data={'target_path': self.current_path})

        @radio_list.control.key_bindings.add("c-d")
        def _key_jump_to_directory(event):
            radio_list._selected_index = 0
            radio_list.values = [(Path(p), p) for p in self.history]
            self.set_title(self.current_path, msg='History')

        @radio_list.control.key_bindings.add("c-c")
        def _key_copy_path(event):
            self.copy_path_clp(self.current_path)

        @radio_list.control.key_bindings.add("escape")
        @radio_list.control.key_bindings.add("f1")
        def _key_exit(event):
            event.app.exit()

        return radio_list

    def get_list_values(self, file_msg : dict = None):
        pwd = self.current_path
        pwds = str(pwd)
        dirs = []
        files = []
        values = []

        if str(pwd.parent) != pwds:
            self.history[str(pwd.parent)] = pwds

        if 'noaccess' in access_type(pwd):
            return {
                'values': [(pwd, HTML(f'<style fg="red"><b>.</b></style>'))],
                'selected_index': 0,
            }

        def render_msg(m):
            return f'<style fg="grey"> - {m}</style>'

        for p in pwd.glob('*'):
            fd = html.escape(p.name)

            msg = ''
            if file_msg and p in file_msg:
                msg = render_msg(file_msg[p])
            else:
                # FEAT: better processing symlinks
                if self.env['show_symlink_paths'] and p.is_symlink():
                    msg = render_msg(p.resolve())

            try:
                if p.is_dir():
                    color = 'red' if 'noaccess' in access_type(p) else 'white'
                    dirs.append((p, HTML(f'<style fg="{color}"><b>{fd}</b></style>{msg}')))
                else:
                    color = 'red' if 'noaccess' in access_type(p) else '#CCCCCC'
                    files.append((p, HTML(f'<style fg="{color}">{fd}</style>{msg}')))
            except:
                files.append((p, HTML(f'<style fg="red">!EXCEPTION: {fd}</style>{msg}')))

        values = sort_files(dirs) + sort_files(files)

        history_index = 0
        if not values:
            values = [(pwd, HTML(f'<style fg="grey"><b>.</b></style>'))]
        elif pwds in self.history:
            history_index = get_index_in_values(values, payload=self.history[pwds])

        return {
            'values': values,
            'selected_index': history_index,
        }

    def change_path(self, new_path):
        self.current_path = new_path.absolute()

    def update_list(self, selected_by_value=None, title_msg=None, file_msg=None):
        self.set_title(self.current_path, msg=title_msg)
        self.list.values, self.list._selected_index = self.get_list_values(file_msg=file_msg).values()
        if selected_by_value:
            self.list._selected_index = get_index_in_values(self.list.values, payload=selected_by_value)

    def move(self, p: Path = None, selected_by_value=None, title_msg=None, file_msg=None, update_list=True):
        p = p if p else self.current_path
        self.change_path(p)
        self.set_title(p, msg=title_msg)
        if update_list:
            self.update_list(selected_by_value=selected_by_value, title_msg=None, file_msg=file_msg)

    def do_open_with(self, path):
        apps = get_os_applications()
        self.set_title(self.current_path, msg='Open with')
        self.list.values = [(open_in_os, 'OS associated')] + [(functools.partial(self.open_in_os_app, app_name=a), a) for a in apps]

        self.list._selected_index = 0
        preselect_app = None
        if str(self.current_path) in self.app_associations:
            preselect_app = self.app_associations[str(self.current_path)]
        elif self.current_path.suffix in self.app_associations:
            preselect_app = self.app_associations[self.current_path.suffix]

        if preselect_app in apps:
            for i, v in enumerate(self.list.values):
                if v[1] == preselect_app:
                    self.list._selected_index = i
                    break
        else:
            # TODO: install?
            pass

    def list_file_actions(self, filepath: Path):
        # filepath = self.current_path
        if filepath.exists():
            funcs = {
                # 'Back': lambda path: move(self.current_path.parent),
                'Copy path': self.copy_path_clp,
                'Open with': self.do_open_with,
                'Rename': self.do_rename,
                'Delete': self.do_delete,
                'Copy': self.do_copy,
                'Move': self.do_move,
                # 'New file': func_file_new,
            }

            if filepath.is_dir():
                add_funcs = {
                    'Create subdirectory': self.do_create_dir,
                    # 'Delete': 'func_dir_delete',
                    # 'Archive': '',
                    # 'Tag date': '',
                    # 'Tag date and time': '',
                }
            else:
                add_funcs = {
                    # 'Delete': 'func_file_delete',
                    # 'Copy to clipboard': '',
                    # 'Copy path': '',
                    # 'Tag date': '',
                    # 'Tag date and time': '',
                }
            funcs = {**funcs, **add_funcs}
        else:
            funcs = {
                'Create this directory': self.do_create_this_dir
            }

        color = 'red' if 'noaccess' in access_type(filepath) else 'grey'

        return [(func, HTML(f'<style fg="{color}">{name}</style>')) for name, func in funcs.items()]

    def copy_path_clp(self, path):
        s = str(path)
        s = repr(s) if ' ' in s else s
        copy_to_clp(s)
        cp = self.current_path
        self.move(path.parent, selected_by_value=path, file_msg={path:'Path copied!'})

    async def show_dialog_as_float(self, dialog, callback, input_data={}):
        """Coroutine."""
        float_ = Float(content=dialog)
        self.root_container.floats.insert(0, float_)

        app = get_app()

        focused_before = app.layout.current_window
        app.layout.focus(dialog)

        dialog_result = await dialog.future

        app.layout.focus(focused_before)

        if float_ in self.root_container.floats:
            self.root_container.floats.remove(float_)

        if dialog_result is not None:
            callback(dialog_result, input_data)

        return dialog_result

    def input_dialog(self, title, label_text, callback, input_data={}, text_area_text=''):
        async def coroutine():
            open_dialog = TextInputDialog(title=title, label_text=label_text, text_area_text=text_area_text)
            await self.show_dialog_as_float(open_dialog, callback, input_data)

        ensure_future(coroutine())




    def open_in_os_app(self, filename: Path, app_name: str = None):
        if self.env['app_associations_save_file']:
            self.app_associations[str(self.current_path)] = app_name
        if app_name and self.current_path.suffix:
            self.app_associations[self.current_path.suffix] = app_name

        if not app_name:
            if str(filename) in self.app_associations:
                app_name = self.app_associations[str(filename)]
            elif filename.suffix in self.app_associations:
                app_name = self.app_associations[filename.suffix]

        return open_in_os(filename, app_name)


    def do_rename(self, filename: Path):
        def callback(new_name, input_data):
            if new_name:
                if (exists := self.current_path.parent / new_name).exists():  # FEAT: overwrite check
                    raise Exception(f'Already exists: {exists}')
                new_path = self.current_path.rename(new_name).absolute()
                self.move(new_path.parent, selected_by_value=new_path)
        self.input_dialog(title='Rename', label_text=f'New name:', callback=callback, text_area_text=self.current_path.name)

    def copy(self, source_path: Path, target_path: str):
        targetp = Path(target_path).expanduser().absolute()
        move = {}
        result = 'unknown'
        if source_path.is_dir():
            if target_path.endswith('/'):
                # If target_path='/target/path/'. Copy `/source/dir` to /target/path/dir`.
                tp = targetp / source_path.name
            else:
                # If target_path='/target/path'. Copy `/source/dir/*` to /target/path/` with replacement.
                tp = targetp

            if tp == source_path:
                move = {
                    'p': tp.parent,
                    'selected_by_value': tp,
                    'file_msg': {tp: 'Copying is not needed :)'}
                }
            else:
                if tp.exists():
                    msg = 'Merged with'
                    result = 'merge'
                else:
                    msg = 'Copied from'
                    result = 'copy'
                create_path_if_needed(tp)
                result_path = shutil.copytree(source_path, tp, dirs_exist_ok=True)
                move = {
                    'p': tp.parent,
                    'selected_by_value': tp,
                    'file_msg': {tp: f'{msg} {source_path}'}
                }
        else:
            if target_path.endswith('/'):
                # If target_path = '/target/path/'. Copy `/source/file` to /target/path/file`.
                tp = targetp / source_path.name
            else:
                # If target_path = '/target/new_filename'. Copy `/source/file` to /target/new_filename`.
                tp = targetp

            if tp == source_path:
                move = {
                    'p': tp.parent,
                    'selected_by_value': tp,
                    'file_msg': {tp: f'Copying is not needed :)'}
                }
                result = 'nocopy'
            else:
                create_path_if_needed(tp.parent)
                if tp.exists():
                    msg = 'Overwritten by'
                    result = 'merge'
                else:
                    msg = 'Copied from'
                    result = 'copy'
                result_path = shutil.copy(source_path, tp)
                move = {
                    'p': tp.parent,
                    'selected_by_value': tp,
                    'file_msg': {tp: f'{msg} {source_path}'}
                }

        return {
            'move': move,
            'result': result
        }

    def callback_copy(self, target_path: str, input_data: dict):
        r = self.copy(input_data['source_path'], target_path)
        self.move(r['move']['p'], selected_by_value=r['move']['selected_by_value'], file_msg=r['move']['file_msg'])
        return r['result']

    def do_copy(self, source_path: Path):
        msg = """If target path ends with `/` the source will be copied to `target/source`.\nIn other cases it will be copied to target or merged with existent.\n\n"""
        self.input_dialog(title='Copy', label_text=msg+f'Copy to:', callback=self.callback_copy, input_data={'source_path': source_path}, text_area_text=str(source_path))

    def callback_move(self, target_path: str, input_data: dict):
        source_path = input_data['source_path']
        sp = Path(source_path)
        tp = Path(target_path)
        if tp.expanduser().absolute() == sp.expanduser().absolute():
            self.move(tp.parent, selected_by_value=tp, file_msg={tp: f'Moving is not needed :)'})
            return

        copy_result = self.callback_copy(target_path, input_data)

        self. callback_delete(source_path, input_data)
        if copy_result == 'merge':
            msg = 'Merged with'
        else:
            msg = 'Moved from'

        mv = tp if target_path.endswith('/') else tp.parent
        selected = (tp/sp.name) if target_path.endswith('/') else tp
        self.move(mv, selected_by_value=selected, file_msg={selected: f'{msg} {source_path}'})


    def do_move(self, source_path: Path):
        msg = """If target path ends with `/` the source will be moved to `target/source`.\nIn other cases it will be moved to target or merged with existent.\n\n"""
        self.input_dialog(title='Move', label_text=msg+f'Move to:', callback=self.callback_move, input_data={'source_path': source_path}, text_area_text=str(source_path))



    def do_create_dir(self, basedir: Path):
        def callback(dirname, input_data):
            if dirname:
                target_dir = basedir / dirname
                target_dir.mkdir(parents=True, exist_ok=True)
                self.move(target_dir, selected_by_value=(basedir / Path(dirname).parts[0]))
        self.input_dialog(title='New directory', label_text=f'Create in {basedir}:', callback=callback)

    def do_create_this_dir(self, basedir: Path):
        basedir.mkdir(parents=True, exist_ok=True)
        self.move(basedir)

    def callback_delete(self, delpath, input_data):
        dp = Path(delpath)
        if dp.is_dir():
            shutil.rmtree(dp)
        else:
            dp.unlink()
        self.move(dp.parent)

    def do_delete(self, filename: Path):
        self.input_dialog(title='Delete', label_text=f'Delete:', callback=self.callback_delete, text_area_text=str(filename))



if __name__ == '__main__':
    import argparse
    argp = argparse.ArgumentParser(description=f"Strider.")
    argp.add_argument('path', nargs='?', default='.', help="Starting path.")
    args = argp.parse_args()

    strider = Strider(current_path=Path(args.path) )
    strider.stride()
    del strider
