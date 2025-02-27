from textual.widgets import TextArea
from textual.reactive import reactive

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

