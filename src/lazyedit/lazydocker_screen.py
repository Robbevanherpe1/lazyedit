from textual.screen import Screen
from textual.widgets import Static
import subprocess
import threading

class LazyDockerScreen(Screen):
    DEFAULT_CSS = """
    LazyDockerScreen {
        layout: vertical;
        color: white;
        text-align: center;
        padding: 2;
        align: center middle;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.process = None

    def compose(self):
        yield Static("LazyDocker is running... Close LazyDocker to return.", id="lazydocker-message")

    def on_mount(self):
        self.run_lazydocker()

    def run_lazydocker(self):
        try:
            self.process = subprocess.Popen(["lazydocker"], text=True)
            threading.Thread(target=self.monitor_lazydocker, daemon=True).start()
        except FileNotFoundError:
            self.app.pop_screen()
            self.app.notify("LazyDocker not found! Please install it.", severity="error")
        except Exception as e:
            self.app.pop_screen()
            self.app.notify(f"Error launching LazyDocker: {str(e)}", severity="error")

    def monitor_lazydocker(self):
        if self.process:
            self.process.wait()
            self.app.call_from_thread(self.exit_lazydocker_screen)

    def exit_lazydocker_screen(self):
        if self.app.screen == self:
            self.app.pop_screen()

    def on_unmount(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            
    def on_key(self, event):
        event.prevent_default()
        event.stop()
