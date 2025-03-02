from textual.widgets import TextArea
from textual.reactive import reactive
from textual.binding import Binding 
from rich.style import Style
from textual.widgets.text_area import TextAreaTheme
import os
import pyperclip
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

@dataclass
class EditOperation:
    text: str
    cursor_location: Union[Tuple[int, int], int]
    selection: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None

my_theme = TextAreaTheme(
    name="EditorTheme",
    base_style=Style(bgcolor="#0C0C0C"),
    cursor_style=Style(color="white", bgcolor="blue"),
    cursor_line_style=Style(bgcolor="#2a2a2a"),
    selection_style=Style(bgcolor="#3b5070"),
    bracket_matching_style=Style(bgcolor="#264f78"),

    syntax_styles = {
        "text": Style(color="#abb2bf"),
        "error": Style(color="#be5046", bgcolor="#22272e"),
        "comment": Style(color="#5c6370", italic=True),
        "comment.block": Style(color="#5c6370", italic=True),
        "comment.block.documentation": Style(color="#5c6370", italic=True),
        "comment.line": Style(color="#5c6370", italic=True),
        "comment.line.double-slash": Style(color="#5c6370", italic=True),
        "comment.line.number-sign": Style(color="#5c6370", italic=True),
        "comment.line.percentage": Style(color="#5c6370", italic=True),
        "constant": Style(color="#d19a66"),
        "constant.builtin": Style(color="#d19a66", bold=True),
        "constant.builtin.boolean": Style(color="#d19a66", bold=True),
        "constant.character": Style(color="#d19a66"),
        "constant.character.escape": Style(color="#d19a66"),
        "constant.character.format": Style(color="#d19a66"),
        "constant.language": Style(color="#d19a66", bold=True),
        "constant.language.null": Style(color="#d19a66", bold=True),
        "constant.language.undefined": Style(color="#d19a66", bold=True),
        "constant.macro": Style(color="#d19a66"),
        "constant.numeric": Style(color="#d19a66"),
        "constant.numeric.binary": Style(color="#d19a66"),
        "constant.numeric.complex": Style(color="#d19a66"),
        "constant.numeric.decimal": Style(color="#d19a66"),
        "constant.numeric.float": Style(color="#d19a66"),
        "constant.numeric.hex": Style(color="#d19a66"),
        "constant.numeric.integer": Style(color="#d19a66"),
        "constant.numeric.octal": Style(color="#d19a66"),
        "constant.other": Style(color="#d19a66"),
        "constant.regexp": Style(color="#d19a66"),
        "constant.rgb-value": Style(color="#d19a66"),
        "boolean": Style(color="#d19a66", bold=True),
        "number": Style(color="#d19a66"),
        "keyword": Style(color="#e06c75"),
        "keyword.control": Style(color="#e06c75"),
        "keyword.control.conditional": Style(color="#e06c75"),
        "keyword.control.directive": Style(color="#e06c75"),
        "keyword.control.flow": Style(color="#e06c75"),
        "keyword.control.import": Style(color="#e06c75"),
        "keyword.control.return": Style(color="#e06c75"),
        "keyword.control.trycatch": Style(color="#e06c75"),
        "keyword.declaration": Style(color="#e06c75"),
        "keyword.declaration.class": Style(color="#e06c75"),
        "keyword.declaration.function": Style(color="#e06c75"),
        "keyword.declaration.method": Style(color="#e06c75"),
        "keyword.declaration.type": Style(color="#e06c75"),
        "keyword.declaration.var": Style(color="#e06c75"),
        "keyword.operator": Style(color="#e06c75"),
        "keyword.operator.arithmetic": Style(color="#e06c75"),
        "keyword.operator.assignment": Style(color="#e06c75"),
        "keyword.operator.comparison": Style(color="#e06c75"),
        "keyword.operator.logical": Style(color="#e06c75"),
        "keyword.operator.new": Style(color="#e06c75"),
        "keyword.other": Style(color="#e06c75"),
        "conditional": Style(color="#e06c75"),
        "repeat": Style(color="#e06c75"),
        "include": Style(color="#e06c75"),
        "exception": Style(color="#e06c75"),
        "operator": Style(color="#e06c75"),
        "operator.assignment": Style(color="#e06c75"),
        "operator.comparison": Style(color="#e06c75"),
        "operator.arithmetic": Style(color="#e06c75"),
        "operator.logical": Style(color="#e06c75"),
        "operator.bitwise": Style(color="#e06c75"),
        "operator.ternary": Style(color="#e06c75"),
        "punctuation": Style(color="#abb2bf"),
        "punctuation.accessor": Style(color="#abb2bf"),
        "punctuation.bracket": Style(color="#abb2bf"),
        "punctuation.bracket.angle": Style(color="#abb2bf"),
        "punctuation.bracket.curly": Style(color="#abb2bf"),
        "punctuation.bracket.round": Style(color="#abb2bf"),
        "punctuation.bracket.square": Style(color="#abb2bf"),
        "punctuation.colon": Style(color="#abb2bf"),
        "punctuation.comma": Style(color="#abb2bf"),
        "punctuation.decorator": Style(color="#e06c75"),
        "punctuation.delimiter": Style(color="#abb2bf"),
        "punctuation.semi": Style(color="#abb2bf"),
        "punctuation.separator": Style(color="#abb2bf"),
        "punctuation.special": Style(color="#61afef"),
        "punctuation.terminator": Style(color="#abb2bf"),
        "string": Style(color="#98c379"),
        "string.documentation": Style(color="#98c379"),
        "string.escape": Style(color="#61afef"),
        "string.heredoc": Style(color="#98c379"),
        "string.interpolated": Style(color="#98c379"),
        "string.other": Style(color="#98c379"),
        "string.quoted": Style(color="#98c379"),
        "string.quoted.double": Style(color="#98c379"),
        "string.quoted.other": Style(color="#98c379"),
        "string.quoted.single": Style(color="#98c379"),
        "string.quoted.triple": Style(color="#98c379"),
        "string.regexp": Style(color="#98c379"),
        "string.special": Style(color="#98c379"),
        "string.template": Style(color="#98c379"),
        "string.unquoted": Style(color="#98c379"),
        "escape": Style(color="#61afef"),
        "variable": Style(color="#abb2bf"),
        "variable.builtin": Style(color="#61afef", bold=True),
        "variable.declaration": Style(color="#abb2bf"),
        "variable.language": Style(color="#c678dd"),
        "variable.language.self": Style(color="#e06c75", italic=True),
        "variable.language.special": Style(color="#c678dd"),
        "variable.language.super": Style(color="#e06c75", italic=True),
        "variable.language.this": Style(color="#e06c75", italic=True),
        "variable.member": Style(color="#abb2bf"),
        "variable.other": Style(color="#abb2bf"),
        "variable.other.constant": Style(color="#d19a66"),
        "variable.other.enummember": Style(color="#d19a66"),
        "variable.other.readwrite": Style(color="#abb2bf"),
        "variable.parameter": Style(color="#abb2bf"),
        "parameter": Style(color="#abb2bf"),
        "property": Style(color="#61afef"),
        "attribute": Style(color="#d19a66"),
        "field": Style(color="#abb2bf"),
        "self": Style(color="#e06c75", italic=True),
        "this": Style(color="#e06c75", italic=True),
        "function": Style(color="#61afef"),
        "function.builtin": Style(color="#61afef", bold=True),
        "function.call": Style(color="#61afef"),
        "function.declaration": Style(color="#61afef", bold=True),
        "function.macro": Style(color="#61afef"),
        "function.method": Style(color="#61afef"),
        "function.method.call": Style(color="#61afef"),
        "function.method.declaration": Style(color="#61afef", bold=True),
        "function.special": Style(color="#61afef", bold=True),
        "method": Style(color="#61afef"),
        "method.call": Style(color="#61afef"),
        "method.declaration": Style(color="#61afef", bold=True),
        "constructor": Style(color="#61afef", bold=True),
        "decorator": Style(color="#e06c75", italic=True),
        "decorator.builtin": Style(color="#e06c75", italic=True, bold=True),
        "type": Style(color="#c678dd"),
        "type.annotation": Style(color="#c678dd"),
        "type.builtin": Style(color="#c678dd", bold=True),
        "type.declaration": Style(color="#c678dd", bold=True),
        "type.definition": Style(color="#c678dd", bold=True),
        "type.parameter": Style(color="#c678dd"),
        "type.primitive": Style(color="#c678dd", bold=True),
        "class": Style(color="#c678dd", bold=True),
        "class.declaration": Style(color="#c678dd", bold=True),
        "class.builtin": Style(color="#c678dd", bold=True),
        "enum": Style(color="#c678dd"),
        "enum.declaration": Style(color="#c678dd", bold=True),
        "enum.member": Style(color="#d19a66"),
        "interface": Style(color="#c678dd"),
        "interface.declaration": Style(color="#c678dd", bold=True),
        "namespace": Style(color="#c678dd"),
        "module": Style(color="#c678dd"),
        "struct": Style(color="#c678dd"),
        "struct.declaration": Style(color="#c678dd", bold=True),
        "typeParameter": Style(color="#c678dd"),
        "union": Style(color="#c678dd"),
        "tag": Style(color="#e06c75"),
        "tag.attribute": Style(color="#61afef"),
        "tag.attribute.name": Style(color="#61afef"),
        "tag.attribute.value": Style(color="#98c379"),
        "tag.delimiter": Style(color="#abb2bf"),
        "tag.name": Style(color="#e06c75"),
        "tag.builtin": Style(color="#e06c75", bold=True),
        "tag.entity": Style(color="#61afef"),
        "tag.id": Style(color="#e06c75"),
        "tag.class": Style(color="#61afef"),
        "css.property": Style(color="#61afef"),
        "css.selector": Style(color="#e06c75"),
        "css.selector.class": Style(color="#61afef"),
        "css.selector.id": Style(color="#e06c75"),
        "css.selector.tag": Style(color="#e06c75"),
        "css.selector.pseudo-class": Style(color="#e06c75"),
        "css.selector.pseudo-element": Style(color="#e06c75"),
        "css.unit": Style(color="#d19a66"),
        "css.color": Style(color="#d19a66"),
        "markup": Style(color="#abb2bf"),
        "markup.bold": Style(color="#abb2bf", bold=True),
        "markup.heading": Style(color="#d19a66", bold=True),
        "markup.heading.1": Style(color="#d19a66", bold=True),
        "markup.heading.2": Style(color="#d19a66", bold=True),
        "markup.heading.3": Style(color="#d19a66", bold=True),
        "markup.heading.4": Style(color="#d19a66", bold=True),
        "markup.heading.5": Style(color="#d19a66", bold=True),
        "markup.heading.6": Style(color="#d19a66", bold=True),
        "markup.italic": Style(color="#abb2bf", italic=True),
        "markup.list": Style(color="#e06c75"),
        "markup.list.numbered": Style(color="#e06c75"),
        "markup.list.unnumbered": Style(color="#e06c75"),
        "markup.quote": Style(color="#5c6370", italic=True),
        "markup.raw": Style(color="#98c379"),
        "markup.strikethrough": Style(color="#abb2bf", strike=True),
        "markup.underline": Style(color="#abb2bf", underline=True),
        "heading": Style(color="#d19a66", bold=True),
        "link": Style(color="#61afef", underline=True),
        "link_url": Style(color="#98c379", underline=True),
        "emphasis": Style(italic=True),
        "strong": Style(bold=True),
        "list": Style(color="#e06c75"),
        "quote": Style(color="#5c6370", italic=True),
        "label": Style(color="#e06c75"),
        "special": Style(color="#61afef"),
        "source": Style(color="#abb2bf"),
        "meta": Style(color="#abb2bf"),
        "meta.block": Style(color="#abb2bf"),
        "meta.function": Style(color="#abb2bf"),
        "meta.tag": Style(color="#abb2bf"),
        "meta.selector": Style(color="#abb2bf"),
        "diff": Style(color="#abb2bf"),
        "diff.plus": Style(color="#3fb950"),
        "diff.minus": Style(color="#f85149"),
        "diff.delta": Style(color="#d29922"),
        "diff.header": Style(color="#61afef", bold=True),
        "git_commit": Style(color="#abb2bf"),
        "git_rebase": Style(color="#abb2bf"),
        "json.property": Style(color="#61afef"),
        "json.string": Style(color="#98c379"),
        "json.number": Style(color="#d19a66"),
        "json.keyword": Style(color="#e06c75"),
        "yaml.key": Style(color="#61afef"),
        "yaml.value": Style(color="#98c379"),
        "yaml.anchor": Style(color="#c678dd"),
        "shell.builtin": Style(color="#61afef", bold=True),
        "shell.command": Style(color="#61afef"),
        "shell.operator": Style(color="#e06c75"),
        "shell.variable": Style(color="#c678dd"),
        "python.builtin": Style(color="#61afef", bold=True),
        "python.decorator": Style(color="#e06c75", italic=True),
        "python.self": Style(color="#e06c75", italic=True),
        "python.magic": Style(color="#61afef", bold=True),
        "python.fstring": Style(color="#98c379"),
        "js.arrow": Style(color="#e06c75"),
        "js.module": Style(color="#e06c75"),
        "js.class": Style(color="#c678dd", bold=True),
        "js.decorator": Style(color="#e06c75", italic=True),
        "js.function": Style(color="#61afef"),
        "js.method": Style(color="#61afef"),
        "js.property": Style(color="#61afef"),
        "js.jsx.tag": Style(color="#e06c75"),
        "js.jsx.attribute": Style(color="#61afef"),
        "js.jsx.text": Style(color="#abb2bf"),
        "rust.attribute": Style(color="#e06c75", italic=True),
        "rust.derive": Style(color="#e06c75", italic=True),
        "rust.macro": Style(color="#61afef"),
        "rust.lifetime": Style(color="#e06c75", italic=True),
        "rust.trait": Style(color="#c678dd"),
        "rust.type": Style(color="#c678dd"),
        "rust.self": Style(color="#e06c75", italic=True),
        "go.package": Style(color="#e06c75"),
        "go.builtin": Style(color="#61afef", bold=True),
        "go.type": Style(color="#c678dd"),
        "go.struct": Style(color="#c678dd"),
        "go.interface": Style(color="#c678dd"),
        "java.annotation": Style(color="#e06c75", italic=True),
        "java.class": Style(color="#c678dd", bold=True),
        "java.import": Style(color="#e06c75"),
        "java.package": Style(color="#e06c75"),
        "java.this": Style(color="#e06c75", italic=True),
        "c.include": Style(color="#e06c75"),
        "c.macro": Style(color="#e06c75"),
        "c.struct": Style(color="#c678dd"),
        "c.type": Style(color="#c678dd"),
        "cpp.class": Style(color="#c678dd", bold=True),
        "cpp.namespace": Style(color="#c678dd"),
        "cpp.template": Style(color="#c678dd"),
        "sql.keyword": Style(color="#e06c75"),
        "sql.function": Style(color="#61afef"),
        "sql.operator": Style(color="#e06c75"),
        "sql.table": Style(color="#c678dd"),
        "sql.column": Style(color="#d19a66"),
        "sql.alias": Style(color="#abb2bf", italic=True),
        "sql.string": Style(color="#98c379"),
        "sql.number": Style(color="#d19a66"),
        "sql.comment": Style(color="#5c6370", italic=True),
        "regex.group": Style(color="#d19a66"),
        "regex.quantifier": Style(color="#e06c75", bold=True),
        "regex.boundary": Style(color="#abb2bf"),
        "regex.characterClass": Style(color="#abb2bf"),
        "regex.alternation": Style(color="#e06c75", bold=True),
        "regex.anchor": Style(color="#d29922", bold=True),
        "regex.captureGroup": Style(color="#98c379"),
        "regex.captureGroupName": Style(color="#98c379", italic=True),
        "markdown.inlineCode": Style(color="#98c379"),
        "markdown.codeBlock": Style(color="#98c379"),
        "markdown.codeBlock.info": Style(color="#61afef"),
        "markdown.link": Style(color="#61afef", underline=True),
        "markdown.list": Style(color="#e06c75"),
        "markdown.emphasis": Style(color="#abb2bf", italic=True),
        "markdown.strong": Style(color="#abb2bf", bold=True),
        "markdown.heading": Style(color="#d19a66", bold=True),
        "markdown.quote": Style(color="#5c6370", italic=True),
        "markdown.hr": Style(color="#5c6370"),
        "toml.key": Style(color="#61afef"),
        "toml.boolean": Style(color="#d19a66", bold=True),
        "toml.string": Style(color="#98c379"),
        "toml.number": Style(color="#d19a66"),
        "docker.keyword": Style(color="#e06c75"),
        "docker.instruction": Style(color="#61afef", bold=True),
        "docker.argument": Style(color="#c678dd"),
        "docker.envvar": Style(color="#d19a66"),
    }
)

class FileEditor(TextArea):
    current_file: str = ""
    editing: bool = reactive(False)
    undo_stack: List[EditOperation] = []
    redo_stack: List[EditOperation] = []
    is_undoing: bool = False
    is_redoing: bool = False
    last_saved_state: Optional[str] = None

    BINDINGS = [
        Binding("up", "cursor_up", "Cursor up", show=False),
        Binding("down", "cursor_down", "Cursor down", show=False),
        Binding("left", "cursor_left", "Cursor left", show=False),
        Binding("right", "cursor_right", "Cursor right", show=False),
        Binding("ctrl+left", "cursor_word_left", "Cursor word left", show=False),
        Binding("ctrl+right", "cursor_word_right", "Cursor word right", show=False),
        Binding("home,ctrl+a", "cursor_line_start", "Cursor line start", show=False),
        Binding("end,ctrl+e", "cursor_line_end", "Cursor line end", show=False),
        Binding("pageup", "cursor_page_up", "Cursor page up", show=False),
        Binding("pagedown", "cursor_page_down", "Cursor page down", show=False),
        Binding("ctrl+shift+left", "cursor_word_left(True)", "Cursor left word select", show=False),
        Binding("ctrl+shift+right", "cursor_word_right(True)", "Cursor right word select", show=False),
        Binding("shift+home", "cursor_line_start(True)", "Cursor line start select", show=False),
        Binding("shift+end", "cursor_line_end(True)", "Cursor line end select", show=False),
        Binding("shift+up", "cursor_up(True)", "Cursor up select", show=False),
        Binding("shift+down", "cursor_down(True)", "Cursor down select", show=False),
        Binding("shift+left", "cursor_left(True)", "Cursor left select", show=False),
        Binding("shift+right", "cursor_right(True)", "Cursor right select", show=False),
        Binding("f6", "select_line", "Select line", show=False),
        Binding("f7", "select_all", "Select all", show=False),
        Binding("backspace", "delete_left", "Delete character left", show=False),
        Binding("ctrl+w", "delete_word_left", "Delete left to start of word", show=False),
        Binding("delete,ctrl+d", "delete_right", "Delete character right", show=False),
        Binding("ctrl+f", "delete_word_right", "Delete right to start of word", show=False),
        Binding("ctrl+x", "cut", "Cut", show=False),
        Binding("ctrl+c", "copy", "Copy", show=False),
        Binding("ctrl+v", "paste", "Paste", show=False),
        Binding("ctrl+u", "delete_to_start_of_line", "Delete to line start", show=False),
        Binding("ctrl+k", "delete_to_end_of_line_or_delete_line", "Delete to line end", show=False),
        Binding("ctrl+shift+k", "delete_line", "Delete line", show=False),
        Binding("ctrl+z", "undo", "Undo", show=False),
        Binding("ctrl+y", "redo", "Redo", show=False),
    ]
    
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
        self.change_timer = None
        self.idle_timer = None
        self.MAX_UNDO_STACK = 100
        
        print(f"Available languages: {self.available_languages}")
        print(f"Available themes: {self.available_themes}")

    def set_content(self, new_content, filename):
        self.current_file = filename
        self.load_text(new_content)
        self.read_only = False
        self.editing = True
        self.disabled = False
        
        self.undo_stack = []
        self.redo_stack = []
        self.last_saved_state = new_content
        self.save_current_state()
        
        self.set_language_from_filename(filename)

    def set_language_from_filename(self, filename):
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
            self.last_saved_state = self.text
            self.app.notify(f"Saved: {self.current_file}")

    def exit_editing(self):
        self.read_only = True
        self.disabled = True
        self.editing = False
        self.app.active_widget = self.app.directory
        self.app.directory.browsing = True

    def action_copy(self) -> None:
        if self.selection:
            try:
                text = self.selected_text
                self.app.clipboard = text
                
                print(f"Attempting to copy text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
                
                pyperclip.copy(text)
                
                clipboard_content = pyperclip.paste()
                if clipboard_content == text:
                    self.app.notify("Text copied to clipboard successfully")
                    print("Copy verification successful")
                else:
                    self.app.notify(f"Copy may have failed - clipboard contains different text")
                    print(f"Expected: '{text[:50]}...'")
                    print(f"Got: '{clipboard_content[:50]}...'")
                    
            except Exception as e:
                error_msg = f"Failed to copy: {str(e)}"
                self.app.notify(error_msg)
                print(error_msg)
                import traceback
                traceback.print_exc()
        else:
            self.app.notify("No text selected")

    def get_current_state(self) -> EditOperation:
        selection = None
        if self.selection:
            selection = (self.selection.start, self.selection.end)
        return EditOperation(
            text=self.text,
            cursor_location=self.cursor_location,
            selection=selection
        )

    def save_current_state(self) -> None:
        if self.is_undoing or self.is_redoing:
            return
            
        current_state = self.get_current_state()
        
        if self.undo_stack and self.undo_stack[-1].text == current_state.text:
            return
            
        self.undo_stack.append(current_state)
        if len(self.undo_stack) > self.MAX_UNDO_STACK:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def apply_state(self, state: EditOperation) -> None:
        self.load_text(state.text)
        
        try:
            if isinstance(state.cursor_location, tuple):
                row, col = state.cursor_location
                row, col = int(row), int(col)
                
                self.cursor_location = (row, col)
            else:
                document = self.document
                row = 0
                col = 0
                remaining = int(state.cursor_location)
                
                for line in document:
                    line_len = len(line) + 1 
                    if remaining < line_len:
                        col = remaining
                        break
                    remaining -= line_len
                    row += 1
                    
                self.cursor_location = (row, col)
            
            if state.selection:
                start, end = state.selection
                if isinstance(start, tuple) and isinstance(end, tuple):
                    from textual.widgets._text_area import Selection
                    self.selection = Selection(start, end)
        except Exception as e:
            print(f"Error in apply_state: {e}")
            import traceback
            traceback.print_exc()
            self.cursor_location = (0, 0)



    def action_undo(self) -> None:
        if len(self.undo_stack) <= 1:
            self.app.notify("Nothing to undo")
            return
            
        self.is_undoing = True
        try:
            current_state = self.get_current_state()
            self.redo_stack.append(current_state)
            
            self.undo_stack.pop()
            previous_state = self.undo_stack[-1]
            
            self.apply_state(previous_state)
            self.app.notify("Undo successful")
        finally:
            self.is_undoing = False

    def action_redo(self) -> None:
        if not self.redo_stack:
            self.app.notify("Nothing to redo")
            return
            
        self.is_redoing = True
        try:
            next_state = self.redo_stack.pop()
            current_state = self.get_current_state()
            self.undo_stack.append(current_state)
            
            self.apply_state(next_state)
            self.app.notify("Redo successful")
        finally:
            self.is_redoing = False

    def on_text_area_changed(self, event) -> None:
        if self.is_undoing or self.is_redoing:
            return
            
        if self.idle_timer:
            self.idle_timer.stop()
            
        self.idle_timer = self.set_timer(0.5, self.save_current_state)

    def on_key(self, event) -> None:
        key_combo = event.key
        
        logical_edit_keys = [
            "enter", "tab", "ctrl+v", "ctrl+x", "delete", "backspace", 
            "ctrl+k", "ctrl+u", "ctrl+w", "ctrl+d", "ctrl+f"
        ]
        
        if key_combo == "space" or key_combo in ".,;:!?()[]{}<>\"'+-*/=":
            self.save_current_state()
        
        elif key_combo in logical_edit_keys:
            self.save_current_state()
    