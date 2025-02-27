from textual.app import App, ComposeResult
from textual.containers import Horizontal, HorizontalScroll, Vertical
from textual.widgets import Static, Input
from textual.reactive import reactive
from rich.panel import Panel
import os
import sys
import subprocess
import threading

if sys.platform == "win32":
    import winpty
else:
    import pty

class Directory(Static):
    def on_mount(self):
        self.update_directory()

    def update_directory(self):
        files = "\n".join(os.listdir("."))
        self.update(Panel(files, title="1 Directory", border_style="yellow"))

    def on_key(self, event):
        pass

class FileEditor(Static):
    content: str = reactive("SELECT * FROM table;")

    def on_mount(self):
        self.update_editor()

    def update_editor(self):
        self.update(Panel(self.content, title="2 File Editor", border_style="yellow"))

    def on_key(self, event):
        if event.key.isprintable():
            self.content += event.key
        elif event.key == "backspace":
            self.content = self.content[:-1]
        self.update_editor()

class Terminal(Static):
    terminal_output: str = reactive("")
    command: str = ""

    def on_mount(self):
        self.update_terminal("Terminal Ready\n")
        self.start_shell()

    def update_terminal(self, output: str):
        self.terminal_output += output
        self.update(Panel(self.terminal_output, title="3 Terminal", border_style="yellow"))

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
        self.update("Commands: (q) Quit     (s) Save File    (Ctrl+1) Directory    (Ctrl+2) File Editor    (Ctrl+3) Terminal")

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
            self.active_widget = self.directory
        elif event.key == "ctrl+2":
            self.active_widget = self.file_editor
        elif event.key == "ctrl+3":
            self.active_widget = self.terminal
        elif hasattr(self.active_widget, "on_key"):
            self.active_widget.on_key(event)

def run():
    MyApp().run()