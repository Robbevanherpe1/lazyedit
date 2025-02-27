from textual.widgets import Static
from textual.reactive import reactive
from rich.console import Console, RenderableType
from rich.text import Text
from rich import box
from rich.panel import Panel
from textual import events
import sys
import subprocess
import threading
import queue
import os

class Terminal(Static):
    DEFAULT_CSS = """
    Terminal {
        color: #007FFF;
        height: 1fr;
        border: solid #007FFF;
        padding: 0 1;
    }
    """
    
    BINDINGS = [
        ("ctrl+c", "send_ctrl_c", "Send Ctrl+C"),
    ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_buffer = ""
        self.output_buffer = []
        self.output_queue = queue.Queue()
        self.cursor_position = 0
        self.process = None
        self.can_focus = True
    
    def on_mount(self):
        self.start_shell()
        self.set_interval(0.1, self.update_output)
    
    def start_shell(self):
        if sys.platform == "win32":
            # Start PowerShell with appropriate parameters
            self.process = subprocess.Popen(
                ["powershell.exe", "-NoLogo"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Start threads to read output
            threading.Thread(target=self._read_output, args=(self.process.stdout,), daemon=True).start()
            threading.Thread(target=self._read_output, args=(self.process.stderr,), daemon=True).start()
        else:
            # For Unix systems, use pty for better terminal emulation
            import pty
            master, slave = pty.openpty()
            self.process = subprocess.Popen(
                ["/bin/bash"],
                stdin=slave,
                stdout=slave,
                stderr=slave,
                text=True,
                start_new_session=True
            )
            os.close(slave)
            
            def read_output():
                with os.fdopen(master, "r") as fd:
                    while True:
                        try:
                            data = fd.read(1)
                            if not data:
                                break
                            self.output_queue.put(data)
                        except (OSError, IOError):
                            break
            
            threading.Thread(target=read_output, daemon=True).start()
    
    def _read_output(self, pipe):
        """Read output from the process pipe and add it to the queue."""
        while self.process and not self.process.poll():
            try:
                line = pipe.readline()
                if not line:
                    break
                self.output_queue.put(line)
            except (OSError, ValueError):
                break
    
    def update_output(self):
        """Process any pending output from the queue."""
        updated = False
        while not self.output_queue.empty():
            try:
                data = self.output_queue.get_nowait()
                self.output_buffer.append(data)
                updated = True
            except queue.Empty:
                break
        
        if updated:
            self.refresh()
    
    def render(self) -> RenderableType:
        """Render the terminal content."""
        # Combine output buffer and current input line
        content = "".join(self.output_buffer[-500:])  # Keep last 500 lines for performance
        prompt_line = f"{self.input_buffer}"
        
        # Create a Text object instead of using console.render
        terminal_content = Text(content + "\n" + prompt_line)
        
        # Return a Panel with the terminal content
        return Panel(
            terminal_content,
            title="PowerShell" if sys.platform == "win32" else "Bash",
            border_style="yellow",
            box=box.ROUNDED
        )
    
    def action_send_ctrl_c(self):
        """Send Ctrl+C to the process."""
        if self.process:
            if sys.platform == "win32":
                self.process.send_signal(subprocess.signal.CTRL_C_EVENT)
            else:
                self.process.send_signal(2)  # SIGINT
    
    def on_key(self, event: events.Key):
        """Handle key events."""
        if event.key == "escape":
            return
        
        if event.key == "enter":
            command = self.input_buffer + "\n"
            self.output_buffer.append(self.input_buffer + "\n")
            self.input_buffer = ""
            self.cursor_position = 0
            
            if self.process and self.process.poll() is None:
                try:
                    self.process.stdin.write(command)
                    self.process.stdin.flush()
                except (BrokenPipeError, IOError):
                    self.output_buffer.append("[Process terminated]\n")
            self.refresh()
            
        elif event.key == "backspace":
            if self.cursor_position > 0:
                self.input_buffer = (
                    self.input_buffer[:self.cursor_position - 1] + 
                    self.input_buffer[self.cursor_position:]
                )
                self.cursor_position -= 1
                self.refresh()
                
        elif event.key == "delete":
            if self.cursor_position < len(self.input_buffer):
                self.input_buffer = (
                    self.input_buffer[:self.cursor_position] + 
                    self.input_buffer[self.cursor_position + 1:]
                )
                self.refresh()
                
        elif event.key == "left":
            if self.cursor_position > 0:
                self.cursor_position -= 1
                self.refresh()
                
        elif event.key == "right":
            if self.cursor_position < len(self.input_buffer):
                self.cursor_position += 1
                self.refresh()
                
        elif event.key == "home":
            self.cursor_position = 0
            self.refresh()
            
        elif event.key == "end":
            self.cursor_position = len(self.input_buffer)
            self.refresh()
            
        elif event.is_printable:
            self.input_buffer = (
                self.input_buffer[:self.cursor_position] + 
                event.character + 
                self.input_buffer[self.cursor_position:]
            )
            self.cursor_position += 1
            self.refresh()
    
    def on_focus(self) -> None:
        self.refresh()
    
    def on_blur(self) -> None:
        self.refresh()
