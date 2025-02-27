from textual.widgets import TextArea
from textual.reactive import reactive
from rich.style import Style
from textual.widgets.text_area import TextAreaTheme

class FileEditor(TextArea):
    current_file: str = ""
    editing: bool = reactive(False)

    my_theme = TextAreaTheme(
    name="EditorTheme",
    cursor_style=Style(color="white", bgcolor="blue"),
    cursor_line_style=Style(bgcolor="yellow"),
    syntax_styles={
        "string": Style(color="red"),
        "comment": Style(color="magenta"),
    }
)
    #TextArea.theme = "EditorTheme"

    def set_content(self, new_content, filename):
        self.current_file = filename
        self.load_text(new_content)
        TextArea.read_only = False
        self.editing = True

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.text)

    def exit_editing(self):
        self.editing = False
        TextArea.read_only = True
        self.app.active_widget = self.app.directory
        self.app.directory.browsing = True

