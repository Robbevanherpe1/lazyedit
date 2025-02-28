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
        
        # Calculate visible height
        visible_height = self.size.height - 2  # Account for panel borders
        if visible_height < 1:
            visible_height = 10  # Default if size not available yet
        
        # Adjust scroll offset to keep selected item visible
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + visible_height:
            self.scroll_offset = self.selected_index - visible_height + 1
        
        # Ensure scroll offset is within bounds
        max_scroll = max(0, len(display_items) - visible_height)
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
        
        # Get visible items based on scroll offset
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
        
        # Add scroll indicators if needed
        title = "Directory"
        if self.scroll_offset > 0:
            title = "↑ " + title
        if self.scroll_offset + visible_height < len(display_items):
            title = title + " ↓"
            
        file_list = "\n".join(file_list_items)
        self.update(Panel(Text.from_markup(file_list), title=title, border_style="#007FFF"))

    def on_key(self, event):
        if not self.browsing:
            return
        
        if event.key == "down" and self.selected_index < len(self.display_items) - 1:
            self.selected_index += 1
            self.render_files()
        elif event.key == "up" and self.selected_index > 0:
            self.selected_index -= 1
            self.render_files()
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
