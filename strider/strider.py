"""Strider"""

import json
import os
import pathlib
import shutil
import html
import functools

from pathlib import Path
from asyncio import ensure_future

from prompt_toolkit import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.application import Application
from prompt_toolkit.widgets import RadioList, Label
from prompt_toolkit.application.current import get_app
from prompt_toolkit.layout.containers import FloatContainer
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.key_binding.key_bindings import KeyBindings, merge_key_bindings
from prompt_toolkit.layout.containers import Float, HSplit

from strider.ptk import TextInputDialog
from strider.clipboard import copy_to_clp
from strider.os import open_in_os, get_os_applications, load_app_associations
from strider.fs import access_type, copy_path


class Strider:
    """Strider"""

    history = {}
    env = {
        'os_path_change': True,
        'show_symlink_paths': True,
        'app_associations_save_file': False
    }

    def __init__(self, current_path: Path = None):
        self.title = Label('Welcome to Strider!')

        current_path = '.' if current_path is None else current_path
        self.current_path = Path(current_path).absolute()
        self.list = self.create_list()

        self._app_associations_file = '/tmp/strider_app_associations_file.json'
        self.app_associations = load_app_associations(self._app_associations_file)

        self.style = self.load_style()

        self.bindings = KeyBindings()

        self.stride()

        Path(self._app_associations_file).write_text(json.dumps(self.app_associations))


    def stride(self):
        """Start striding."""
        first_selected = None
        if not self.current_path.is_dir():
            first_selected = self.current_path
            self.history[str(self.current_path.parent)] = str(self.current_path)
            self.current_path = self.current_path.parent
        self.update_list(selected_by_value=first_selected, file_msg={first_selected: "I'm here!"})

        self.root_container = FloatContainer(
            content=HSplit([self.title, self.list]),
            floats=[]
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
        """Load style."""
        style = Style.from_dict({})

        # FEAT
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


    def set_title(self, p: Path, msg=None):
        """Set the main title."""
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
        """Create the main list."""
        default = None
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
                r = copy_path(Path(source_path), str(input_data['target_path'])+'/')
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
        def _key_exit(event):
            event.app.exit()

        return radio_list


    @staticmethod
    def sort_files_in_list(list_sets):
        """Sort files in the list of sets that represent the main list."""
        def sort_func(s):
            return str(s[0]).lower()

        return sorted(list_sets, key=sort_func)


    @staticmethod
    def get_index_in_values(values, payload=None, text=None, default_index=0):
        """Get index in the list of sets that represent the main list."""
        for num, p in enumerate(values):
            if payload and (str(p[0]) == payload or p[0] == payload):
                return num
            if text and p[1] == text:
                return num
        return default_index

    def get_list_values(self, file_msg : dict = None):
        """Get the list of files for the main list."""
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

        values = self.sort_files_in_list(dirs) + self.sort_files_in_list(files)

        history_index = 0
        if not values:
            values = [(pwd, HTML(f'<style fg="grey"><b>.</b></style>'))]
        elif pwds in self.history:
            history_index = self.get_index_in_values(values, payload=self.history[pwds])

        return {
            'values': values,
            'selected_index': history_index,
        }


    def update_list(self, selected_by_value=None, title_msg=None, file_msg=None):
        """
        Update list of files in the main list.
        :param selected_by_value:
        :param title_msg:
        :param file_msg:
        :return:
        """
        self.set_title(self.current_path, msg=title_msg)
        self.list.values, self.list._selected_index = self.get_list_values(file_msg=file_msg).values()
        if selected_by_value:
            self.list._selected_index = self.get_index_in_values(self.list.values, payload=selected_by_value)

    def move(self, p: Path = None, selected_by_value=None, title_msg=None, file_msg=None, update_list=True):
        """
        Move to the path.
        :param p:
        :param selected_by_value:
        :param title_msg:
        :param file_msg:
        :param update_list:
        :return:
        """
        p = p if p else self.current_path
        self.current_path = p.absolute()
        self.set_title(p, msg=title_msg)
        if self.env['os_path_change']:
            os.chdir(self.current_path)
        if update_list:
            self.update_list(selected_by_value=selected_by_value, title_msg=None, file_msg=file_msg)

    def do_open_with(self, path):
        """Show "Open with" menu."""
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
            # FEAT
            pass

    def list_file_actions(self, filepath: Path):
        """Show menu with actions."""
        if filepath.exists():
            funcs = {
                # 'Back': lambda path: move(self.current_path.parent),  # FEAT
                'Copy path': self.copy_path_clp,
                'Open with': self.do_open_with,
                'Rename': self.do_rename,
                'Delete': self.do_delete,
                'Copy': self.do_copy,
                'Move': self.do_move,
                # 'New file': do_file_new,  # FEAT
            }

            if filepath.is_dir():
                add_funcs = {
                    'Create subdirectory': self.do_create_dir,
                    # 'Archive': do_archive,  # FEAT
                }
            else:
                add_funcs = {
                    # 'Copy content to clipboard': do_file_copy_content,  # FEAT
                }
            funcs = {**funcs, **add_funcs}
        else:
            funcs = {
                'Create this directory': self.do_create_this_dir
            }

        color = 'red' if 'noaccess' in access_type(filepath) else 'grey'

        return [(func, HTML(f'<style fg="{color}">{name}</style>')) for name, func in funcs.items()]


    def copy_path_clp(self, path):
        """Copy path."""
        s = str(path)
        s = repr(s) if ' ' in s else s
        copy_to_clp(s)
        cp = self.current_path
        self.move(path.parent, selected_by_value=path, file_msg={path: 'Path copied!'})


    def open_in_os_app(self, filename: Path, app_name: str = None):
        """Opening in OS associated application."""
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
        """Doing rename."""
        def callback(new_name, input_data):
            if new_name:
                if (exists := self.current_path.parent / new_name).exists():  # FEAT: overwrite check
                    raise Exception(f'Already exists: {exists}')
                new_path = self.current_path.rename(new_name).absolute()
                self.move(new_path.parent, selected_by_value=new_path)
        self.input_dialog(title='Rename', label_text=f'New name:', callback=callback, text_area_text=self.current_path.name)




    def callback_copy(self, target_path: str, input_data: dict):
        """Callback to doing copy path."""
        r = copy_path(input_data['source_path'], target_path)
        self.move(r['move']['p'], selected_by_value=r['move']['selected_by_value'], file_msg=r['move']['file_msg'])
        return r['result']

    def do_copy(self, source_path: Path):
        """Doing copy path."""
        msg = """If target path ends with `/` the source will be copied to `target/source`.\nIn other cases it will be copied to target or merged with existent.\n\n"""
        self.input_dialog(title='Copy', label_text=msg+f'Copy to:', callback=self.callback_copy, input_data={'source_path': source_path}, text_area_text=str(source_path))


    def callback_move(self, target_path: str, input_data: dict):
        """Callback to doing move path."""
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
        """Doing move path."""
        msg = """If target path ends with `/` the source will be moved to `target/source`.\nIn other cases it will be moved to target or merged with existent.\n\n"""
        self.input_dialog(title='Move', label_text=msg+f'Move to:', callback=self.callback_move, input_data={'source_path': source_path}, text_area_text=str(source_path))



    def do_create_dir(self, basedir: Path):
        """Doing "Create directory"."""
        def callback(dirname, input_data):
            if dirname:
                target_dir = basedir / dirname
                target_dir.mkdir(parents=True, exist_ok=True)
                self.move(target_dir, selected_by_value=(basedir / Path(dirname).parts[0]))
        self.input_dialog(title='New directory', label_text=f'Create in {basedir}:', callback=callback)


    def do_create_this_dir(self, basedir: Path):
        """Doing "Create this directory"."""
        basedir.mkdir(parents=True, exist_ok=True)
        self.move(basedir)


    def callback_delete(self, delpath, input_data):
        """Callback to delete path."""
        dp = Path(delpath)
        if dp.is_dir():
            shutil.rmtree(dp)
        else:
            dp.unlink()
        self.move(dp.parent)

    def do_delete(self, filename: Path):
        """Show menu to delete path."""
        self.input_dialog(title='Delete', label_text=f'Delete:', callback=self.callback_delete, text_area_text=str(filename))


    async def show_dialog_as_float(self, dialog, callback, input_data={}):
        """Coroutine. Show dialog as float."""
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
        """Construct input dialog."""
        async def coroutine():
            open_dialog = TextInputDialog(title=title, label_text=label_text, text_area_text=text_area_text)
            await self.show_dialog_as_float(open_dialog, callback, input_data)
        ensure_future(coroutine())
