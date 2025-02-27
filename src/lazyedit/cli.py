from textual.app import App, ComposeResult
from textual.containers import Horizontal, HorizontalScroll, Vertical
from textual.widgets import Static
from textual.reactive import reactive
from rich.panel import Panel
import os

class Directory(Static):
    def on_mount(self):
        files = "\n".join(os.listdir("."))
        self.update(Panel(files, title="Directory", border_style="yellow"))

class FileEditor(Static):
    content: str = reactive("SELECT * FROM table;aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    def on_mount(self):
        self.update(Panel(self.content, title="File Editor", border_style="yellow"))

    def on_key(self, event):
        if event.key.isprintable():
            self.content += event.key
        elif event.key == "backspace":
            self.content = self.content[:-1]

    def watch_content(self, old_value, new_value):
        self.update(Panel(new_value, title="File Editor", border_style="yellow"))

class Terminal(Static):
    def on_mount(self):
        self.update(Panel("_", title="Terminal", border_style="yellow"))

class CommandFooter(Static):
    def on_mount(self):
        self.update("Commands: (q) Quit     (s) Save File")

class MyApp(App):
    CSS = """
    Screen {
        layout: vertical;
    }
    Horizontal {
        layout: horizontal;
        height: 1fr;
    }
    Directory {
        width: 25%;
        height: 100%;
    }
    FileEditor {
        height: 100%;
    }
    Terminal {
        height: 30%;
    }
    CommandFooter {
        dock: bottom;
        height: auto;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Directory()
            with Vertical():
                with HorizontalScroll():
                    yield FileEditor()
                yield Terminal()
        yield CommandFooter()

    def on_key(self, event):
        if event.key.lower() == "q":
            self.exit()

def run():
    MyApp().run()
