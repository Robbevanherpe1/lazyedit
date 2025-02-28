# LazyEdit - The Effortless Code Editor
  
Code editing shouldn't be hard work. Be lazy. Be efficient.

LazyEdit is a lightweight, terminal-based code editor with an integrated PowerShell terminal designed for developers who want a streamlined editing experience without leaving the command line.

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
That's it! No complex setup or configuration required.

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

### **Editing Files**
- Switch to **File Editing Mode** (`Ctrl+3`) to edit the opened file
- Use standard keyboard navigation (**arrows, Home, End**) to move around
- Save your changes with **`Ctrl+S`**

### **Using the Terminal**
- Switch to **Terminal Mode** (`Ctrl+5`) to use the PowerShell terminal
- Execute commands as you would in a normal PowerShell window
- The terminal shows your current directory relative to where LazyEdit was launched

---

## ⌨️ Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Ctrl+Q` | Quit LazyEdit |
| `Ctrl+S` | Save current file |
| `Ctrl+2` | Switch to Directory Mode |
| `Ctrl+3` | Switch to File Editing Mode |
| `Ctrl+5` | Switch to Terminal Mode |
| `Ctrl+C` | Send interrupt signal (in Terminal) |
| `Ctrl+L` | Clear terminal screen |
| `Space`  | Open selected file (in Directory Mode) |
| `Up/Down` | Navigate files or text |
| `Home/End` | Move to start/end of line |

---

## 💻 Development
Want to contribute or run from source? Follow these steps:
```sh
# Clone the repository
git clone https://github.com/yourusername/lazyedit.git
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
│       ├── directory.py    # File browser functionality
│       ├── fileEditor.py   # Text editing functionality
│       ├── gui.py          # Main application interface
│       └── terminal.py     # PowerShell terminal integration
├── pyproject.toml
├── README.md
└── LICENSE.txt
```

---

## 📝 License
LazyEdit is distributed under the terms of the **MIT license**.

Made with ❤️ by **Robbe**

_When you're too lazy to open a full IDE, but too productive for Notepad._

