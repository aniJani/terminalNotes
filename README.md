# Terminal Notes

A beautiful and powerful notes application that runs entirely in your terminal with a built-in text editor.

## 🌟 Features

- **Built-in Terminal Text Editor**: Full-featured text editor that runs entirely in your terminal
  - Real-time cursor navigation with arrow keys
  - Line numbers and syntax highlighting
  - Save with `Ctrl+S`, Cancel with `Ctrl+C`
  - Visual interface with Rich panels and status bar
- **Markdown Support**: Create and manage notes in markdown format
- **Notebook Organization**: Organize notes in notebooks (folders)
- **Powerful Search**: Search through your notes content
- **Beautiful Interface**: Rich terminal interface with colors and styling
- **Template Support**: Use templates for consistent note structure
- **Quick Inbox**: Rapidly capture thoughts and ideas
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **No External Dependencies**: No need for vim, nano, or external editors

## 📋 Prerequisites

- **Python 3.7 or higher**
- **pip** (Python package installer)
- **Git** (for cloning the repository)

### Check Your Python Version
```bash
python --version
# or
python3 --version
```

If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/).

## 🚀 Installation

### Method 1: Quick Install from GitHub (Recommended for Users)

This method installs Terminal Notes as a global command on your system:

```bash
pip install git+https://github.com/aniJani/terminalNotes.git
```

**That's it!** After installation, you can use the `notes` command anywhere in your terminal.

**Verify installation:**
```bash
notes --help
```

### Method 2: Development Installation (For Contributors)

This method is perfect if you want to contribute to the project or modify the code:

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/terminal-notes.git
   cd terminal-notes
   ```

2. **Create a virtual environment (strongly recommended)**
   ```bash
   # On Windows Command Prompt
   python -m venv venv
   venv\Scripts\activate

   # On Windows PowerShell
   python -m venv venv
   venv\Scripts\Activate.ps1

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install in development mode**
   ```bash
   pip install -e .
   ```
   
   The `-e` flag installs the package in "editable" mode, meaning changes to the code will be reflected immediately without reinstalling.

4. **Verify installation**
   ```bash
   notes --help
   ```

### Method 3: Manual Installation (Without pip)

If you prefer not to install the package globally:

1. **Download the repository**
   - Click the green "Code" button on GitHub
   - Select "Download ZIP"
   - Extract the ZIP file to your desired location

2. **Navigate to the project directory**
   ```bash
   cd path/to/terminal-notes
   ```

3. **Install dependencies manually**
   ```bash
   pip install typer>=0.16.0 rich>=14.1.0
   ```

4. **Run directly with Python**
   ```bash
   python notes.py --help
   ```

### Installation Troubleshooting

#### "notes: command not found" after installation

**On Windows:**
1. **Check if Python Scripts is in PATH:**
   ```cmd
   echo %PATH%
   ```
   Look for a path like `C:\Users\YourName\AppData\Local\Programs\Python\Python3X\Scripts`

2. **If not in PATH, add it manually:**
   - Open System Properties → Advanced → Environment Variables
   - Edit the PATH variable
   - Add your Python Scripts directory

3. **Alternative: Use Python module syntax**
   ```bash
   python -m notes --help
   ```

**On macOS/Linux:**
1. **Check if pip install location is in PATH:**
   ```bash
   echo $PATH
   python3 -m site --user-base
   ```

2. **Add to PATH if needed (add to ~/.bashrc or ~/.zshrc):**
   ```bash
   export PATH="$PATH:$(python3 -m site --user-base)/bin"
   ```

3. **Reload your shell:**
   ```bash
   source ~/.bashrc  # or ~/.zshrc
   ```

#### "Permission denied" errors

**On Windows:**
- Run Command Prompt as Administrator
- Or use: `pip install --user git+https://github.com/aniJani/terminalNotes.git`

**On macOS/Linux:**
- Use: `pip3 install --user git+https://github.com/aniJani/terminalNotes.git`
- Or install with sudo: `sudo pip3 install git+https://github.com/aniJani/terminalNotes.git`

#### Virtual Environment Issues

If you're using a virtual environment and the `notes` command isn't found:

1. **Make sure your virtual environment is activated:**
   ```bash
   # You should see (venv) or similar in your prompt
   which python  # On Unix
   where python  # On Windows
   ```

2. **Reinstall in the virtual environment:**
   ```bash
   pip install -e .
   ```

### System Requirements Check

Before installing, verify you have the required components:

```bash
# Check Python version (3.7+ required)
python --version

# Check pip is available
pip --version

# Check git is available (for Method 1 and 2)
git --version
```

**Expected output:**
```
Python 3.11.5
pip 23.2.1
git version 2.41.0
```

## 🎯 Quick Start

After installation, you can use the `notes` command directly:

```bash
# Create your first note (opens the built-in editor)
notes new "My First Note"

# List all your notes
notes list

# Edit an existing note
notes edit "My First Note"

# View a note with beautiful markdown rendering
notes show "My First Note"

# Search through your notes (Search functions currently not working (in development))
notes search "keyword"

# Quick capture to inbox
notes add "Important reminder for later"

# Delete a note
notes delete "My First Note"
```

## 🖥️ Terminal Editor Usage

The built-in terminal editor provides a modern editing experience:

### Keyboard Shortcuts
- **Arrow Keys**: Navigate cursor
- **Enter**: New line
- **Backspace**: Delete character/join lines
- **Ctrl+S**: Save and exit
- **Ctrl+C**: Cancel without saving

### Editor Features
- **Line Numbers**: Professional editor feel
- **Real-time Status**: See line/column position and character count
- **Visual Cursor**: Block cursor shows your exact position
- **Multiple Lines**: Full support for multi-line editing

## 📚 Advanced Usage

### Organizing with Notebooks
```bash
# Create a note in a specific notebook
notes new "Meeting Notes" --notebook "Work"

# Create a note using a template
notes new "Daily Standup" --template "meeting"
```

### Templates
Create templates in the templates directory to standardize your notes:

1. Find your notes directory: `notes list` will show the path
2. Navigate to the `templates` folder
3. Create `.md` files that will be used as templates

## 🛠️ Configuration

Notes are stored in your system's application data directory:
- **Windows**: `%APPDATA%\terminal-notes-app\notes\`
- **macOS**: `~/Library/Application Support/terminal-notes-app/notes/`
- **Linux**: `~/.local/share/terminal-notes-app/notes/`

## 🐛 Troubleshooting

### Common Issues

**"notes: command not found"**
- Ensure you've installed the package: `pip install -e .`
- Check if your Python Scripts directory is in PATH
- Try restarting your terminal

**"ModuleNotFoundError: No module named 'typer'"**
- Install dependencies: `pip install typer rich`
- Make sure you're in the correct virtual environment

**Editor not working on non-Windows systems**
- The application includes a fallback text input mode
- You'll see prompts to enter content and type `---SAVE---` to save

**Permission errors**
- On Unix systems, you might need to make the script executable
- Or run with `python3 -m notes` instead

### Getting Help

If you encounter issues:

1. **Check Python and pip versions**
   ```bash
   python --version
   pip --version
   ```

2. **Reinstall the package**
   ```bash
   pip uninstall terminal-notes
   pip install -e .
   ```

3. **Run in debug mode**
   ```bash
   python notes.py --help
   ```

### Development Setup
```bash
git clone https://github.com/yourusername/terminal-notes.git
cd terminal-notes
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

