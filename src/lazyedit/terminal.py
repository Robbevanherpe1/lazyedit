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
import keyboard

class Terminal(Static):
    DEFAULT_CSS = """
    Terminal {
        color: #FFFFFF;
        height: 1fr;
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
        self.terminal_size = (24, 80) 
        self.visible_lines = 20
        self.prompt = "PS > "
        self.is_active = False
        self._updating = False
    
    def on_mount(self):
        self.terminal_size = (self.size.height, self.size.width)
        self.visible_lines = self.terminal_size[0] - 2
        self.start_shell()
        self.set_interval(0.05, self.update_output)
    
    def on_resize(self, event):
        if hasattr(self, "size"):
            self.terminal_size = (self.size.height, self.size.width)
            self.visible_lines = self.terminal_size[0] - 2
    
    def start_shell(self):
        self.process = subprocess.Popen(
            ["powershell.exe", "-NoLogo"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        threading.Thread(target=self._read_output, args=(self.process.stdout,), daemon=True).start()
        threading.Thread(target=self._read_output, args=(self.process.stderr,), daemon=True).start()
        self.output_buffer.append(f"{self.prompt}")
    
    def _read_output(self, pipe):
        while self.process and self.process.poll() is None:
            try:
                line = pipe.readline()
                if not line:
                    char = pipe.read(1)
                    if not char:
                        break
                    self.output_queue.put(char)
                else:
                    self.output_queue.put(line)
            except (OSError, ValueError):
                break
    
    def update_output(self):
        updated = False
        while not self.output_queue.empty():
            try:
                data = self.output_queue.get_nowait()
                if isinstance(data, bytes):
                    try:
                        text = data.decode('utf-8', errors='replace')
                    except UnicodeDecodeError:
                        text = data.decode('latin-1')
                    self.output_buffer.append(text)
                else:
                    self.output_buffer.append(data)
                updated = True
            except queue.Empty:
                break
        
        if len(self.output_buffer) > 5000:
            self.output_buffer = self.output_buffer[-5000:]
        
        if updated:
            self.renderable = self.render()
            self.refresh(layout=True)
    
    def render(self) -> RenderableType:
        if not hasattr(self, "output_buffer") or self.output_buffer is None:
            return Panel(
                "",
                title="PowerShell",
                border_style="#555555",
                box=box.ROUNDED
            )
            
        content = "".join(self.output_buffer)
        content_lines = content.split("\n")
        visible_content_lines = content_lines[-self.visible_lines:] if content_lines else []
        visible_content = "\n".join(visible_content_lines)
        
        if self.has_focus and self.is_active:
            cursor = "█"
            input_line = (
                self.input_buffer[:self.cursor_position] + 
                cursor + 
                self.input_buffer[self.cursor_position:]
            )
            
            if not visible_content.endswith(self.prompt):
                visible_content += self.prompt
                
            if visible_content.endswith(self.prompt):
                visible_content = visible_content[:-len(self.prompt)] + self.prompt + input_line
        
        terminal_content = Text(visible_content)
        
        border_style = "#007FFF" if self.is_active else "#555555"
        
        return Panel(
            terminal_content,
            title="PowerShell",
            border_style=border_style,
            box=box.ROUNDED
        )
    
    def action_send_ctrl_c(self):
        if not self.is_active:
            return
            
        if self.process and self.process.poll() is None:
            try:
                self.process.send_signal(subprocess.signal.CTRL_C_EVENT)
            except:
                self.write_to_terminal("\x03")
    
    def write_to_terminal(self, data):
        if not self.process or self.process.poll() is not None:
            return
        
        try:
            self.process.stdin.write(data)
            self.process.stdin.flush()
        except (BrokenPipeError, IOError):
            self.output_buffer.append("[Process terminated]\n")
    
    def on_key(self, event: events.Key):
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("q"):
            return
        
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("2"):
            return
            
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("3"):
            return
            
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("5"):
            return
        
        if not self.has_focus or not self.is_active:
            return
        
        event.prevent_default()
        event.stop()
        
        if event.key == "escape":
            return
        
        if event.key == "enter":
            command = self.input_buffer + "\n"
            
            if self.output_buffer and self.output_buffer[-1].endswith(self.prompt):
                self.output_buffer[-1] = self.output_buffer[-1][:-len(self.prompt)]
            
            self.output_buffer.append(f"{self.prompt}{self.input_buffer}\n")
            
            self.input_buffer = ""
            self.cursor_position = 0
            
            self.write_to_terminal(command)
            
            self.output_buffer.append(f"{self.prompt}")
            
            self.renderable = self.render()
            self.refresh(layout=True)
            
        elif event.key == "backspace":
            if self.cursor_position > 0:
                self.input_buffer = (
                    self.input_buffer[:self.cursor_position - 1] + 
                    self.input_buffer[self.cursor_position:]
                )
                self.cursor_position -= 1
                self.renderable = self.render()
                self.refresh(layout=True)
                
        elif event.key == "delete":
            if self.cursor_position < len(self.input_buffer):
                self.input_buffer = (
                    self.input_buffer[:self.cursor_position] + 
                    self.input_buffer[self.cursor_position + 1:]
                )
                self.renderable = self.render()
                self.refresh(layout=True)
                
        elif event.key == "left":
            if self.cursor_position > 0:
                self.cursor_position -= 1
                self.renderable = self.render()
                self.refresh(layout=True)
                
        elif event.key == "right":
            if self.cursor_position < len(self.input_buffer):
                self.cursor_position += 1
                self.renderable = self.render()
                self.refresh(layout=True)
                
        elif event.key == "home":
            self.cursor_position = 0
            self.renderable = self.render()
            self.refresh(layout=True)
            
        elif event.key == "end":
            self.cursor_position = len(self.input_buffer)
            self.renderable = self.render()
            self.refresh(layout=True)
            
        elif event.key == "tab":
            self.write_to_terminal("\t")
            self.renderable = self.render()
            self.refresh(layout=True)
            
        elif event.key == "ctrl+l":
            self.output_buffer = [f"{self.prompt}"]
            self.renderable = self.render()
            self.refresh(layout=True)
            
        elif event.is_printable:
            self.input_buffer = (
                self.input_buffer[:self.cursor_position] + 
                event.character + 
                self.input_buffer[self.cursor_position:]
            )
            self.cursor_position += 1
            self.renderable = self.render()
            self.refresh(layout=True)
    
    def on_focus(self) -> None:
        self.renderable = self.render()
        self.refresh(layout=True)
    
    def on_blur(self) -> None:
        self.renderable = self.render()
        self.refresh(layout=True)
        
    def on_unmount(self) -> None:
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.process.kill()
                
    def refresh(self, **kwargs):
        super().refresh(**kwargs)
