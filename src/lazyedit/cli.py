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
        self.update(Panel(files, title="Directory", border_style="yellow"))

class FileEditor(Static):
    content: str = reactive("SELECT * FROM table;")

    def on_mount(self):
        self.update_editor()

    def update_editor(self):
        self.update(Panel(self.content, title="File Editor", border_style="yellow"))

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