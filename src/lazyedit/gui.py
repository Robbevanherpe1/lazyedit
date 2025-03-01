import keyboard
import signal
from textual.app import App, ComposeResult
from textual.containers import Horizontal, HorizontalScroll, Vertical
from textual.widgets import Static
from textual.events import Key
from textual.reactive import reactive
from textual.binding import Binding
import sys
import os

from .lazydocker_screen import LazyDockerScreen
from .lazygit_screen import LazyGitScreen

from .fileEditor import FileEditor
from .directory import Directory
from .terminal import Terminal

class CommandFooter(Static):
    def on_mount(self):
        self.update("Commands: (Ctrl+q) Quit   (Enter) Create File   (Backspace) Delete File   (Ctrl+s) Save File   (Ctrl+2) Dir Mode    (Ctrl+3) Edit Mode    (Ctrl+5) Terminal   (Ctrl+g) Git mode")

class MyApp(App):
    CSS = """
    Screen {
    layout: vertical;
    background: #0C0C0C;
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
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+c", "handle_copy", "Copy"),
    ]
    
    current_mode = reactive("directory")

    def __init__(self):
        super().__init__()
        self.active_widget = None
        self.cursor_row = 0
        self.cursor_column = 0

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

    def on_mount(self):
        def sigint_handler(sig, frame):
            self.notify("Use Ctrl+Q to quit")
            return True
        
        signal.signal(signal.SIGINT, sigint_handler)
        
        self.directory.browsing = True
        self.file_editor.editing = False
        self.terminal.is_active = False

    def action_handle_copy(self) -> None:
        focused = self.focused
        if focused and hasattr(focused, "action_copy"):
            focused.action_copy()
        else:
            self.notify("Use Ctrl+Q to quit")
    
    def action_quit(self) -> None:
        self.exit()
        os.system("cls" if os.name == "nt" else "clear")

    def on_key(self, event):
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("q"):
            self.action_quit()
            return
        
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("2"):
            self.switch_to_directory_mode()
            return
            
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("3"):
            self.switch_to_editor_mode()
            return
            
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("5"):
            self.switch_to_terminal_mode()
            return
        
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("g"):
            self.push_screen(LazyGitScreen())
            return
        
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("d"):
            self.push_screen(LazyDockerScreen())
            return
        
        if self.current_mode == "directory":
            if keyboard.is_pressed("ctrl") and keyboard.is_pressed("s"):
                return
            if hasattr(self.directory, "on_key"):
                self.directory.on_key(event)
                
        elif self.current_mode == "editor":
            if keyboard.is_pressed("ctrl") and keyboard.is_pressed("s"):
                self.file_editor.save_file()
                return
            if hasattr(self.file_editor, "on_key"):
                self.file_editor.on_key(event)
                
        elif self.current_mode == "terminal":
            if hasattr(self.terminal, "on_key"):
                self.terminal.on_key(event)
    
    def switch_to_directory_mode(self):
        self.current_mode = "directory"
        self.directory.browsing = True
        self.file_editor.editing = False
        self.terminal.is_active = False
        self.active_widget = self.directory
        self.directory.focus()
        self.file_editor.exit_editing()
        self.refresh_ui()
    
    def switch_to_editor_mode(self):
        self.current_mode = "editor"
        self.directory.browsing = False
        self.file_editor.editing = True
        self.terminal.is_active = False
        self.active_widget = self.file_editor
        self.file_editor.focus()
        self.refresh_ui()
    
    def switch_to_terminal_mode(self):
        self.current_mode = "terminal"
        self.directory.browsing = False
        self.file_editor.editing = False
        self.terminal.is_active = True
        self.active_widget = self.terminal
        self.terminal.focus()
        self.file_editor.exit_editing()
        self.refresh_ui()
    
    def refresh_ui(self):
        self.directory.render_files()
        
        if hasattr(self.terminal, "output_buffer"):
            self.terminal.renderable = self.terminal.render()
            self.terminal.refresh(layout=True)
            
        if hasattr(self.file_editor, "refresh"):
            self.file_editor.refresh()

def run():
    try:
        MyApp().run()
    except KeyboardInterrupt:
        print("Application terminated by user")
