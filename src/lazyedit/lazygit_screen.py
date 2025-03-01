from textual.screen import Screen
from textual.widgets import Static
import subprocess
import threading

class LazyGitScreen(Screen):
    DEFAULT_CSS = """
    LazyGitScreen {
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
        yield Static("LazyGit is running... Close LazyGit to return.", id="lazygit-message")

    def on_mount(self):
        self.run_lazygit()

    def run_lazygit(self):
        try:
            self.process = subprocess.Popen(["lazygit"], text=True)
            threading.Thread(target=self.monitor_lazygit, daemon=True).start()
        except FileNotFoundError:
            self.app.pop_screen()
            self.app.notify("LazyGit not found! Please install it.", severity="error")
        except Exception as e:
            self.app.pop_screen()
            self.app.notify(f"Error launching LazyGit: {str(e)}", severity="error")

    def monitor_lazygit(self):
        if self.process:
            self.process.wait()
            self.app.call_from_thread(self.exit_lazygit_screen)

    def exit_lazygit_screen(self):
        if self.app.screen == self:
            self.app.pop_screen()

    def on_unmount(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()

    def on_key(self, event):
        if event.key == "ctrl+q":
            if self.process and self.process.poll() is None:
                self.process.terminate()
            self.app.exit()
