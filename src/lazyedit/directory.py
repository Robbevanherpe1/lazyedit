from textual.widgets import Static
from textual.reactive import reactive
from rich.panel import Panel
from rich.text import Text
import os


class Directory(Static):
    selected_index: int = reactive(0)
    files: list = []
    browsing: bool = reactive(True)
    expanded_folders: set = set()

    def on_mount(self):
        self.update_directory()

    def update_directory(self):
        self.files = os.listdir(".")
        self.render_files()

    def render_files(self):
        display_items = []
        
        for file_path in sorted(self.files):
            display_items.append((file_path, 0))  
           
            if os.path.isdir(file_path) and file_path in self.expanded_folders:
                try:
                    subfiles = [os.path.join(file_path, f) for f in os.listdir(file_path)]
                    for subfile in sorted(subfiles):
                        display_items.append((subfile, 1))
                except (PermissionError, OSError):
                    pass
        
        file_list_items = []
        for i, (file_path, indent_level) in enumerate(display_items):
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
            
            if i == self.selected_index:
                file_list_items.append(f"[green]{display_text}[/green]")
            else:
                file_list_items.append(display_text)
        
        file_list = "\n".join(file_list_items)
        self.update(Panel(Text.from_markup(file_list), title="Directory", border_style="#007FFF"))
        
        self.display_items = display_items

    def on_key(self, event):
        if not self.browsing:
            return
        
        if event.key == "down" and self.selected_index < len(self.display_items) - 1:
            self.selected_index += 1
        elif event.key == "up" and self.selected_index > 0:
            self.selected_index -= 1
        elif event.key == "space":
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
                    print(f"Error opening file: {e}")
        
        self.render_files()
