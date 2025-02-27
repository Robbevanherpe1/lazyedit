from textual.widgets import Static
from textual.reactive import reactive
from rich.panel import Panel
import sys
import subprocess
import threading

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
