"""Prompt toolkit components."""

from asyncio import Future
from prompt_toolkit.application.current import get_app
from prompt_toolkit.widgets import (
    RadioList,
    Button,
    Dialog,
    Label,
    TextArea,
)

from prompt_toolkit.layout.containers import (
    HSplit,
)
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.filters import Condition


class StriderRadioList(RadioList):
    def get_selected_value(self):
        return self.values[self._selected_index][0]

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
            text=text_area_text,
            focus_on_click=True
        )
        self.text_area.control.key_bindings = KeyBindings()

        # Select line to easy press delete for pasting new path
        self.text_area.buffer._set_cursor_position(0)
        self.text_area.buffer.start_selection()
        self.text_area.buffer.selection_state.enter_shift_mode()
        self.text_area.buffer._set_cursor_position(len(text_area_text))

        ok_button = Button(text="OK", handler=accept)
        cancel_button = Button(text="Cancel", handler=cancel)

        @self.text_area.control.key_bindings.add("escape")
        @ok_button.control.key_bindings.add("escape")
        @cancel_button.control.key_bindings.add("escape")
        def _key_close_dialog(event):
            self.future.set_result(None)

        @Condition
        def is_select_mode() -> bool:
            return self.text_area.buffer.selection_state is not None

        @self.text_area.control.key_bindings.add("enter", filter=is_select_mode)
        def _key_stop_typing(event):
            # Stop selection before going forward.
            self.text_area.buffer.exit_selection()

        self.dialog = Dialog(
            title=title,
            body=HSplit([Label(text=label_text), self.text_area]),
            buttons=[ok_button, cancel_button],
            width=D(preferred=80),
            modal=True,
        )


    def __pt_container__(self):
        return self.dialog
