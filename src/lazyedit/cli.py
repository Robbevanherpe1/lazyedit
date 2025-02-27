from textual.app import App, ComposeResult
from textual.containers import Horizontal, HorizontalScroll, Vertical
from textual.widgets import Static, Input, TextArea
from textual.reactive import reactive
from rich.panel import Panel
from rich.text import Text
import os
import sys
import subprocess
import threading

if sys.platform == "win32":
    import winpty
else:
    import pty

class Directory(Static):
    selected_index: int = reactive(0)
    files: list = []
    browsing: bool = reactive(True)

    def on_mount(self):
        self.update_directory()

    def update_directory(self):
        self.files = os.listdir(".")
        self.render_files()

    def render_files(self):
        file_list = "\n".join(
            f"[green]{file}[/green]" if i == self.selected_index else file
            for i, file in enumerate(self.files)
        )
        self.update(Panel(Text.from_markup(file_list), title="Directory", border_style="yellow"))

    def on_key(self, event):
        if not self.browsing:
            return
        if event.key == "down" and self.selected_index < len(self.files) - 1:
            self.selected_index += 1
        elif event.key == "up" and self.selected_index > 0:
            self.selected_index -= 1
        elif event.key == "space":
            selected_file = self.files[self.selected_index]
            if os.path.isfile(selected_file):
                with open(selected_file, "r", encoding="utf-8", errors="ignore") as f:
                    file_content = f.read()
                self.app.file_editor.set_content(file_content, selected_file)
        self.render_files()

class FileEditor(TextArea):
    current_file: str = ""
    editing: bool = reactive(False)

    def set_content(self, new_content, filename):
        self.current_file = filename
        self.load_text(new_content)
        self.editing = True

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.text)

    def exit_editing(self):
        self.editing = False
        self.app.active_widget = self.app.directory
        self.app.directory.browsing = True

class Terminal(Static):
    terminal_output: str = reactive("")
    command: str = ""

    def on_mount(self):
        self.update_terminal("Terminal Ready\n")
        self.start_shell()

    def update_terminal(self, output: str):
        self.terminal_output += output
        self.update(Panel(self.terminal_output, title="Terminal", border_style="yellow"))

    def start_shell(self):
        if sys.platform == "win32":
            self.process = subprocess.Popen(
                ["cmd.exe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
        else:
            master, slave = pty.openpty()
            self.process = subprocess.Popen(
                ["/bin/bash"], stdin=slave, stdout=slave, stderr=slave, text=True, bufsize=1, universal_newlines=True
            )

            def read_output():
                with open(master, "r") as out:
                    while True:
                        line = out.readline()
                        if line:
                            self.update_terminal(line)

            threading.Thread(target=read_output, daemon=True).start()

    def on_key(self, event):
        if event.key.isprintable():
            self.command += event.key
        elif event.key == "enter":
            self.update_terminal(f"> {self.command}\n")
            self.process.stdin.write(self.command + "\n")
            self.process.stdin.flush()
            self.command = ""
        elif event.key == "backspace":
            self.command = self.command[:-1]

class CommandFooter(Static):
    def on_mount(self):
        self.update("Commands: (q) Quit     (Ctrl+S) Save File    (Ctrl+1) Directory Mode    (Ctrl+2) File Editing Mode    (Ctrl+3) Terminal")

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

    def __init__(self):
        super().__init__()
        self.active_widget = None

    def compose(self) -> ComposeResult:
        self.directory = Directory()
        self.file_editor = FileEditor()
        self.terminal = Terminal()
        self.footer = CommandFooter()

        with Horizontal():
            yield self.directory
            with Vertical():
                with HorizontalScroll():
                    yield self.file_editor
                yield self.terminal
        yield self.footer

        self.active_widget = self.directory

    def on_key(self, event):
        if event.key.lower() == "q":
            self.exit()
        elif event.key == "ctrl+1":
            self.file_editor.exit_editing()
            self.active_widget = self.directory
            self.directory.browsing = True
        elif event.key == "ctrl+2":
            self.active_widget = self.file_editor
            self.directory.browsing = False
        elif event.key == "ctrl+3":
            self.file_editor.exit_editing()
            self.active_widget = self.terminal
        elif event.key == "ctrl+s" and self.active_widget == self.file_editor:
            self.file_editor.save_file()
        elif hasattr(self.active_widget, "on_key"):
            self.active_widget.on_key(event)

def run():
    MyApp().run()