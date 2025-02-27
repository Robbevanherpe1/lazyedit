from textual.widgets import TextArea
from textual.reactive import reactive
from rich.style import Style
from textual.widgets.text_area import TextAreaTheme

# Define the theme outside the class
my_theme = TextAreaTheme(
    name="EditorTheme",
    cursor_style=Style(color="white", bgcolor="blue"),
    cursor_line_style=Style(bgcolor="#2a2a2a"),
    syntax_styles={
        "string": Style(color="red"),
        "comment": Style(color="magenta"),
    }
)

class FileEditor(TextArea):
    current_file: str = ""
    editing: bool = reactive(False)
    
    def __init__(self, *args, **kwargs):
        # First initialize with default theme
        super().__init__(*args, **kwargs)
        # Then register our custom theme
        self.register_theme(my_theme)
        # Now we can set the theme
        self.theme = "EditorTheme"

    def set_content(self, new_content, filename):
        self.current_file = filename
        self.load_text(new_content)
        self.read_only = False
        self.editing = True
        self.disabled = False

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.text)

    def exit_editing(self):
        self.read_only = True
        self.disabled = True
        self.editing = False
        self.app.active_widget = self.app.directory
        self.app.directory.browsing = True
