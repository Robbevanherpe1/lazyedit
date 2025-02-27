from textual.widgets import Static
from textual.reactive import reactive
from rich.panel import Panel
from rich.text import Text
import os


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