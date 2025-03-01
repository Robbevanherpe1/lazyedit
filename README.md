# LazyEdit - The Effortless TUI Code Editor

[![PyPI - Version](https://img.shields.io/pypi/v/lazyedit.svg)](https://pypi.org/project/lazyedit)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lazyedit.svg)](https://pypi.org/project/lazyedit)


**_When you're too lazy to open a full IDE, but too productive for Notepad._**
  
Code editing shouldn't be hard work. Be lazy. Be efficient.

LazyEdit is a lightweight, terminal-based code editor with an integrated PowerShell terminal designed for developers who want a streamlined editing experience without leaving the command line.

![preview](previewNew.gif)

## ✨ Features
- **All-in-One Interface**: File browser, text editor, and PowerShell terminal in a single window
- **Keyboard-Driven**: Navigate and edit efficiently with intuitive keyboard shortcuts
- **Syntax Highlighting**: Makes your code more readable and easier to understand
- **Integrated Terminal**: Run commands without switching applications
- **Lightweight**: Minimal resource usage compared to full IDEs
- **Windows-Optimized**: Built specifically for Windows with PowerShell integration

---

## 📋 Table of Contents
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Keyboard Shortcuts](#-keyboard-shortcuts)
- [Development](#-development)
- [License](#-license)

---

## 🚀 Installation
```sh
pip install lazyedit
```
Optional lazyGit when u want to use git feature
```sh
pip install lazygit
```
That's it! No complex setup or configuration required.

If it fails to run your Python Scripts folder might not be in the system PATH.

Run Temporary:
```ps
$env:Path += ";C:\Users\YourUserName\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts"
```

Run Permanent:
```
[System.Environment]::GetEnvironmentVariable("Path", "User") -split ";" | Out-File -FilePath "$env:TEMP\PathBackup.txt"
[System.Environment]::SetEnvironmentVariable("Path", $newPath, "User")
$newPath = [System.Environment]::GetEnvironmentVariable("Path", "User") + ";C:\Users\YourUserName\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts"
```

Now try running lazyedit again.
---

## 🏃‍♂️ Quick Start
After installation, simply run:
```sh
lazyedit
```
You'll be greeted with a three-panel interface:
- **Left panel**: File browser
- **Main panel**: Text editor
- **Bottom panel**: PowerShell terminal

---
## 📖 Usage Guide
### **File Navigation**
- Use **Directory Mode** (`Ctrl+2`) to browse files
- Navigate with **arrow keys** to select a file
- Press **Space** to open the selected file in the editor
- Press **Enter** to create a new file
- Press **Backspace** to delete a file

### **Editing Files**
- Switch to **File Editing Mode** (`Ctrl+3`) to edit the opened file
- Use standard keyboard navigation (**arrows, Home, End**) to move around
- Save your changes with **`Ctrl+S`**

### **Using the Terminal**
- Switch to **Terminal Mode** (`Ctrl+5`) to use the PowerShell terminal
- Execute commands as you would in a normal PowerShell window
- The terminal shows your current directory relative to where LazyEdit was launched

## 🐙 Git Integration
lazyedit by Jesse Duffield's : [lazygit](https://github.com/jesseduffield/lazygit)
LazyEdit includes **LazyGit** for effortless repository management.

### **Launching LazyGit**
- Switch to **Git Mode** using `Ctrl+g`.
- This opens **LazyGit** in a separate floating window.
- You can manage branches, commits, merges, and pull requests from LazyGit without leaving LazyEdit.

### **Common Git Commands via LazyGit**
| Action           | Command in LazyGit |
|-----------------|------------------|
| Stage changes  | Select file + Press `<Space>` |
| Unstage changes | Select file + Press `<U>` |
| Commit changes  | Press `<C>` and enter message |
| Push to remote  | Press `<P>` |
| Pull from remote | Press `<Shift+P>` |
| Switch branches | Press `<B>` |
| Create new branch | Press `<N>` |
| Merge branches | Press `<M>` |
| Stash changes | Press `<S>` |
| View logs & history | Press `<L>` |
| Quit LazyGit | Press `<Q>` |

---

## ⌨️ Keyboard Shortcuts

### **General Shortcuts**
| Shortcut  | Action                         |
|-----------|--------------------------------|
| <kbd>Ctrl</kbd> + <kbd>Q</kbd>  | Quit LazyEdit                  |
| <kbd>Ctrl</kbd> + <kbd>2</kbd>  | Switch to Directory Mode       |
| <kbd>Ctrl</kbd> + <kbd>3</kbd>  | Switch to File Editing Mode    |
| <kbd>Ctrl</kbd> + <kbd>5</kbd>  | Switch to Terminal Mode        |
| <kbd>Ctrl</kbd> + <kbd>g</kbd>  | Switch to Git Mode        |

### **📂 Directory Mode**
| Shortcut    | Action                                     |
|-------------|--------------------------------------------|
| <kbd>Enter</kbd>     | Create a new file in the current directory |
| <kbd>Backspace</kbd> | Delete the selected file                  |
| <kbd>Space</kbd>     | Open the selected file in the text editor  |
| <kbd>↑</kbd> / <kbd>↓</kbd>  | Navigate the file list             |

### **📝 File Editing Mode**
| Shortcut   | Action                                  |
|------------|-----------------------------------------|
| <kbd>Ctrl</kbd> + <kbd>S</kbd>  | Save the currently open file |
| <kbd>↑</kbd> / <kbd>↓</kbd>  | Move cursor line up/down               |
| <kbd>Home</kbd> / <kbd>End</kbd>  | Move to start/end of the current line  |
| <kbd>Ctrl</kbd> + <kbd>A</kbd>  | Select all text |
| <kbd>Ctrl</kbd> + <kbd>X</kbd>  | Cut selected text |
| <kbd>Ctrl</kbd> + <kbd>C</kbd>  | Copy selected text |
| <kbd>Ctrl</kbd> + <kbd>V</kbd>  | Paste copied text |
| <kbd>Ctrl</kbd> + <kbd>Z</kbd>  | Undo last action |
| <kbd>Ctrl</kbd> + <kbd>Y</kbd>  | Redo last undone action |
| <kbd>Ctrl</kbd> + <kbd>←</kbd>  | Move cursor one word left |
| <kbd>Ctrl</kbd> + <kbd>→</kbd>  | Move cursor one word right |
| <kbd>Shift</kbd> + <kbd>←</kbd>  | Select text left |
| <kbd>Shift</kbd> + <kbd>→</kbd>  | Select text right |
| <kbd>Ctrl</kbd> + <kbd>Backspace</kbd>  | Delete word left |
| <kbd>Ctrl</kbd> + <kbd>Delete</kbd>  | Delete word right |
| <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>K</kbd>  | Delete current line |
| <kbd>f6</kbd>  | Select the current line |
| <kbd>f7</kbd>  | Select all text in the document |

### **💻 Terminal Mode**
| Shortcut   | Action                                    |
|------------|-------------------------------------------|
| <kbd>Ctrl</kbd> + <kbd>C</kbd>  | Send interrupt signal (in Terminal)      |
| <kbd>Ctrl</kbd> + <kbd>L</kbd>  | Clear terminal screen                    |


---

## 💻 Development
Want to contribute or run from source? Follow these steps:
```sh
# Clone the repository
git clone https://github.com/Robbevanherpe1/lazyedit.git
cd lazyedit

# Create and activate development environment
hatch env create
hatch shell

# Install in development mode
pip install -e .

# Run LazyEdit
lazyedit
```

### **Project Structure**
```plaintext
lazyedit/
├── src/
│   └── lazyedit/
│       ├── __init__.py
│       ├── __about__.py
|       ├── lazygit_screen.py # Lazygit screen integration
│       ├── directory.py      # File browser functionality
│       ├── fileEditor.py     # Text editing functionality
│       ├── gui.py            # Main application interface
│       └── terminal.py       # PowerShell terminal integration
├── tests/
│       ├── directory/
│       ├── fileEdit/
│       ├── terminal/
│       ├── __init__.py
│       └── test_basic.py
├── pyproject.toml
├── README.md
└── LICENSE.txt
```

---

## 📝 License
LazyEdit is distributed under the terms of the **EPL license**.

Made with ❤️ by **Robbe*

_Inspiration by Jesse Duffield's lazygit and lazydocker_
