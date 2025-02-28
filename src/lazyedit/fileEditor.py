from textual.widgets import TextArea
from textual.reactive import reactive
from rich.style import Style
from textual.widgets.text_area import TextAreaTheme
import os

my_theme = TextAreaTheme(
    name="EditorTheme",
    #base_style=Style(color="#f8f8f2", bgcolor="none"),
    cursor_style=Style(color="white", bgcolor="blue"),
    cursor_line_style=Style(bgcolor="#2a2a2a"),
    #gutter_style=Style(color="#90908a", bgcolor="#272822"),
    selection_style=Style(bgcolor="#44475a"),
    bracket_matching_style=Style(bgcolor="#3a3d41"),

    syntax_styles={
        "string": Style(color="#a8ff60"),
        "string.special": Style(color="#ffd242"),
        "comment": Style(color="#7a7a7a", italic=True),
        "keyword": Style(color="#ff8000", bold=True),
        "function": Style(color="#52aeff"),
        "function.builtin": Style(color="#52aeff", bold=True),
        "function.method": Style(color="#52aeff"),
        "variable": Style(color="#c6c6c6"),
        "variable.builtin": Style(color="#ff628c"),
        "operator": Style(color="#ff8000"),
        "property": Style(color="#52aeff"),
        "tag": Style(color="#ff8000"),
        "constant": Style(color="#ffd242"),
        "constant.builtin": Style(color="#ffd242", bold=True),
        "type": Style(color="#52aeff", bold=True),
        "attribute": Style(color="#bfa6fe"),
        "number": Style(color="#ff628c"),
        "parameter": Style(color="#c6c6c6"),
        
        "decorator": Style(color="#bfa6fe"),
        "class": Style(color="#52aeff", bold=True),
        "self": Style(color="#ff628c", italic=True),
        "module": Style(color="#a8ff60"),
        "punctuation": Style(color="#f8f8f2"),
        "punctuation.bracket": Style(color="#f8f8f2"),
        "punctuation.delimiter": Style(color="#f8f8f2"),
        
        "boolean": Style(color="#ffd242"),
        "conditional": Style(color="#ff8000", bold=True),
        "repeat": Style(color="#ff8000", bold=True),
        "label": Style(color="#bfa6fe"),
        "include": Style(color="#ff8000"),
        "exception": Style(color="#ff8000", bold=True),
        "namespace": Style(color="#52aeff"),
        "type.builtin": Style(color="#52aeff", bold=True),
        "variable.parameter": Style(color="#c6c6c6"),
        "escape": Style(color="#ffd242"),
        
        "heading": Style(color="#ff8000", bold=True),
        "link": Style(color="#52aeff", underline=True),
        "link_url": Style(color="#a8ff60", underline=True),
        "emphasis": Style(italic=True),
        "strong": Style(bold=True),
        
        "tag": Style(color="#ff8000"),
        "attribute": Style(color="#bfa6fe"),
        
        "text": Style(color="#f8f8f2"),
        "error": Style(color="red", bgcolor="#272822"),
    }
)

class FileEditor(TextArea):
    current_file: str = ""
    editing: bool = reactive(False)
    
    EXTENSION_TO_LANGUAGE = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".md": "markdown",
        ".c": "c",
        ".cpp": "cpp",
        ".h": "c",
        ".hpp": "cpp",
        ".java": "java",
        ".go": "go",
        ".rs": "rust",
        ".rb": "ruby",
        ".php": "php",
        ".sh": "bash",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".toml": "toml",
        ".xml": "xml",
        ".sql": "sql",
        ".lua": "lua",
        ".dart": "dart",
        ".swift": "swift",
        ".kt": "kotlin",
        ".scala": "scala",
        ".r": "r",
        ".jsx": "javascript",
        ".tsx": "typescript",
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_line_numbers = True
        self.tab_behavior = "indent"
        
        self.register_theme(my_theme)
        self.theme = "EditorTheme"
        
        print(f"Available languages: {self.available_languages}")
        print(f"Available themes: {self.available_themes}")

    def set_content(self, new_content, filename):
        self.current_file = filename
        self.load_text(new_content)
        self.read_only = False
        self.editing = True
        self.disabled = False
        
        self.set_language_from_filename(filename)

    def set_language_from_filename(self, filename):
        """Set the appropriate language for syntax highlighting based on file extension"""
        if not filename:
            return
            
        _, ext = os.path.splitext(filename.lower())
        
        print(f"File extension: {ext}")
        
        if ext in self.EXTENSION_TO_LANGUAGE:
            language = self.EXTENSION_TO_LANGUAGE[ext]

            print(f"Selected language: {language}")
            print(f"Available languages: {self.available_languages}")
            
            if language in self.available_languages:
                self.language = language
                self.app.notify(f"Syntax highlighting enabled: {language}")
                self.set_timer(0.5, self.debug_highlights)
            else:
                self.language = None
                self.app.notify(f"Language '{language}' not available for highlighting")
        else:
            self.language = None

    def debug_highlights(self):
        """Debug method to print the highlights being generated"""
        if hasattr(self, "_highlights") and self._highlights:
            self.app.notify(f"Found {len(self._highlights)} highlight groups")
            for line_idx, highlights in enumerate(self._highlights):
                if highlights:
                    print(f"Line {line_idx} highlights: {highlights}")
                    if line_idx > 5:
                        break
        else:
            self.app.notify("No highlights found")

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.text)
            self.app.notify(f"Saved: {self.current_file}")

    def exit_editing(self):
        self.read_only = True
        self.disabled = True
        self.editing = False
        self.app.active_widget = self.app.directory
        self.app.directory.browsing = True
