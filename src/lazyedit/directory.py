from textual.widgets import Static, Input, Label, Button
from textual.reactive import reactive
from textual.containers import Container, Horizontal
from rich.panel import Panel
from rich.text import Text
import os
import shutil


class DeleteConfirmDialog(Container):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        
    def compose(self):
        file_name = os.path.basename(self.file_path)
        yield Label(f"Delete '{file_name}'?")
        
        with Horizontal(id="button_container"):
            yield Button("Yes", id="yes_button", variant="primary")
            yield Button("No", id="no_button")
        
    def on_mount(self):
        self.query_one("#yes_button").focus()
        
    def on_button_pressed(self, event):
        if event.button.id == "yes_button":
            try:
                if os.path.isdir(self.file_path):
                    shutil.rmtree(self.file_path)
                else:
                    os.remove(self.file_path)
                self.app.directory.update_directory()
                self.app.notify(f"Deleted: {os.path.basename(self.file_path)}")
            except Exception as e:
                self.app.notify(f"Error deleting file: {str(e)}", severity="error")
        
        self.app.directory.browsing = True
        self.remove()
    
    def on_key(self, event):
        if event.key == "left":
            self.query_one("#yes_button").focus()
        elif event.key == "right":
            self.query_one("#no_button").focus()
        elif event.key == "escape":
            self.app.directory.browsing = True
            self.remove()


class FileNameDialog(Container):
    def __init__(self, directory_path):
        super().__init__()
        self.directory_path = directory_path
        
    def compose(self):
        yield Label("Enter file name:")
        yield Input(id="filename_input")
        
    def on_mount(self):
        self.query_one(Input).focus()
        
    def on_input_submitted(self, event):
        filename = event.value.strip()
        if filename:
            file_path = os.path.join(self.directory_path, filename)
            
            try:
                with open(file_path, "w") as f:
                    pass
                
                self.app.directory.update_directory()
                self.app.directory.browsing = True
                self.remove()
                
                if os.path.isfile(file_path):
                    self.app.file_editor.set_content("", file_path)
            except Exception as e:
                self.app.notify(f"Error creating file: {str(e)}", severity="error")
                self.remove()
    
    def on_key(self, event):
        if event.key == "escape":
            self.app.directory.browsing = True
            self.remove()


class Directory(Static):
    selected_index: int = reactive(0)
    files: list = []
    browsing: bool = reactive(True)
    expanded_folders: set = set()
    scroll_offset: int = reactive(0)

    def on_mount(self):
        self.update_directory()

    def update_directory(self):
        self.files = os.listdir(".")
        self.render_files()

    def get_nested_files(self, folder_path, current_indent):
        nested_items = []
        try:
            subfiles = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]
            for subfile in sorted(subfiles):
                nested_items.append((subfile, current_indent))
                if os.path.isdir(subfile) and subfile in self.expanded_folders:
                    nested_items.extend(self.get_nested_files(subfile, current_indent + 1))
        except (PermissionError, OSError):
            pass
        return nested_items

    def render_files(self):
        display_items = []
        
        for file_path in sorted(self.files):
            display_items.append((file_path, 0))
            
            if os.path.isdir(file_path) and file_path in self.expanded_folders:
                display_items.extend(self.get_nested_files(file_path, 1))
        
        self.display_items = display_items
        
        visible_height = self.size.height - 2 
        if visible_height < 1:
            visible_height = 26
        
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + visible_height:
            self.scroll_offset = self.selected_index - visible_height + 1
    
        max_scroll = max(0, len(display_items) - visible_height)
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
        
        visible_items = display_items[self.scroll_offset:self.scroll_offset + visible_height]
        
        file_list_items = []
        for i, (file_path, indent_level) in enumerate(visible_items):
            actual_index = i + self.scroll_offset
            prefix = "    " * indent_level
            file_name = os.path.basename(file_path)
            
            if os.path.isdir(file_path):
                if file_path in self.expanded_folders:
                    icon = "▼ "
                else:
                    icon = "▶ "
            else:
                icon = "  "
                
            display_text = f"{prefix}{icon}{file_name}"
            
            if actual_index == self.selected_index:
                file_list_items.append(f"[green]{display_text}[/green]")
            else:
                file_list_items.append(display_text)
        
        title = "Directory"
        if self.scroll_offset > 0:
            title = "↑ " + title
        if self.scroll_offset + visible_height < len(display_items):
            title = title + " ↓"
            
        file_list = "\n".join(file_list_items)
        
        border_style = "#007FFF" if self.browsing and self.app.current_mode == "directory" else "#555555"
        
        self.update(Panel(Text.from_markup(file_list), title=title, border_style=border_style))

    def on_key(self, event):
        if self.app.current_mode != "directory" or not self.browsing:
            return
        
        event.prevent_default()
        event.stop()
        
        if event.key == "down" and self.selected_index < len(self.display_items) - 1:
            self.selected_index += 1
            self.render_files()
        elif event.key == "up" and self.selected_index > 0:
            self.selected_index -= 1
            self.render_files()
        elif event.key == "enter":
            if self.selected_index < len(self.display_items):
                selected_path, _ = self.display_items[self.selected_index]
                
                if os.path.isdir(selected_path):
                    directory_path = selected_path
                else:
                    directory_path = os.path.dirname(selected_path)
                    if not directory_path:
                        directory_path = "."
                
                self.browsing = False
                dialog = FileNameDialog(directory_path)
                self.app.mount(dialog)
            else:
                self.browsing = False
                dialog = FileNameDialog(".")
                self.app.mount(dialog)
        elif event.key == "backspace" or event.key == "delete":
            if self.selected_index < len(self.display_items):
                selected_path, _ = self.display_items[self.selected_index]
                self.browsing = False
                dialog = DeleteConfirmDialog(selected_path)
                self.app.mount(dialog)
                
        elif event.key == "space":
            if self.selected_index < len(self.display_items):
                selected_path, _ = self.display_items[self.selected_index]
                
                if os.path.isdir(selected_path):
                    if selected_path in self.expanded_folders:
                        self.expanded_folders.remove(selected_path)
                    else:
                        self.expanded_folders.add(selected_path)
                    self.render_files()
                elif os.path.isfile(selected_path):
                    try:
                        with open(selected_path, "r", encoding="utf-8", errors="ignore") as f:
                            file_content = f.read()
                        self.app.file_editor.set_content(file_content, selected_path)
                    except Exception as e:
                        self.app.notify(f"Error opening file: {str(e)}", severity="error")
