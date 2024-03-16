from asyncio import Future
from prompt_toolkit.application.current import get_app
from prompt_toolkit.widgets import (
    Button,
    Dialog,
    Label,
    TextArea,
)

from prompt_toolkit.layout.containers import (
    HSplit,
)


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


    def __pt_container__(self):
        return self.dialog