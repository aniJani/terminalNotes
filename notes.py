import typer
import os
import subprocess
import shutil
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.panel import Panel

APP_NAME = "terminal-notes-app"
APP_DIR = typer.get_app_dir(APP_NAME)
NOTES_DIR = os.path.join(APP_DIR, "notes")
TEMPLATES_DIR = os.path.join(APP_DIR, "templates")

os.makedirs(NOTES_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

console = Console()
app = typer.Typer(
    help="Notes in your terminal.",
    rich_markup_mode="rich",
)


def terminal_editor(initial_content: str = "", title: str = "Edit Note") -> str:
    """Simple terminal-based text editor using Rich"""
    lines = initial_content.split("\n") if initial_content else [""]
    cursor_row = 0
    cursor_col = 0

    def render_editor():
        # Header
        header = Panel(
            f"[bold cyan]{title}[/bold cyan]\n"
            f"[dim]Ctrl+S: Save & Exit | Ctrl+C: Cancel | Arrow keys: Navigate[/dim]",
            style="blue",
        )

        content_lines = []
        for i, line in enumerate(lines):
            line_num = f"{i+1:3d} "
            if i == cursor_row:
                displayed_line = line[:cursor_col] + "█" + line[cursor_col:]
                content_lines.append(
                    f"[bold yellow]{line_num}[/bold yellow][white]{displayed_line}[/white]"
                )
            else:
                content_lines.append(f"[dim]{line_num}[/dim]{line}")

        while len(content_lines) < 15:
            line_num = f"{len(content_lines)+1:3d} "
            content_lines.append(f"[dim]{line_num}[/dim]~")

        content_panel = Panel(
            "\n".join(content_lines), title="Content", border_style="green"
        )

        status = f"Line {cursor_row + 1}, Col {cursor_col + 1} | {len(lines)} lines | {sum(len(line) for line in lines)} chars"
        status_panel = Panel(status, style="blue")

        console.print(header)
        console.print(content_panel)
        console.print(status_panel)

    console.clear()

    try:
        import msvcrt  # works for Windows systems

        while True:
            console.clear()
            render_editor()

            key = msvcrt.getch()

            if key == b"\x03":  # Ctrl+C
                raise KeyboardInterrupt
            elif key == b"\x13":  # Ctrl+S
                return "\n".join(lines)
            elif key == b"\x08":  # Backspace
                if cursor_col > 0:
                    line = lines[cursor_row]
                    lines[cursor_row] = line[: cursor_col - 1] + line[cursor_col:]
                    cursor_col -= 1
                elif cursor_row > 0:
                    # Join with previous line
                    cursor_col = len(lines[cursor_row - 1])
                    lines[cursor_row - 1] += lines[cursor_row]
                    lines.pop(cursor_row)
                    cursor_row -= 1
            elif key == b"\r":  # Enter
                line = lines[cursor_row]
                lines[cursor_row] = line[:cursor_col]
                lines.insert(cursor_row + 1, line[cursor_col:])
                cursor_row += 1
                cursor_col = 0
            elif key == b"\xe0":  # Special keys (arrows)
                key2 = msvcrt.getch()
                if key2 == b"H":  # Up arrow
                    if cursor_row > 0:
                        cursor_row -= 1
                        cursor_col = min(cursor_col, len(lines[cursor_row]))
                elif key2 == b"P":  # Down arrow
                    if cursor_row < len(lines) - 1:
                        cursor_row += 1
                        cursor_col = min(cursor_col, len(lines[cursor_row]))
                elif key2 == b"K":  # Left arrow
                    if cursor_col > 0:
                        cursor_col -= 1
                    elif cursor_row > 0:
                        cursor_row -= 1
                        cursor_col = len(lines[cursor_row])
                elif key2 == b"M":  # Right arrow
                    if cursor_col < len(lines[cursor_row]):
                        cursor_col += 1
                    elif cursor_row < len(lines) - 1:
                        cursor_row += 1
                        cursor_col = 0
            else:
                try:
                    char = key.decode("utf-8")
                    if char.isprintable():
                        line = lines[cursor_row]
                        lines[cursor_row] = line[:cursor_col] + char + line[cursor_col:]
                        cursor_col += 1
                except UnicodeDecodeError:
                    pass

    except ImportError:
        # Fallback for non-Windows systems or if msvcrt not available
        console.print(f"\n[bold cyan]Editing: {title}[/bold cyan]")
        console.print("[bold yellow]Multi-line input mode[/bold yellow]")
        console.print(
            "[dim]Enter your content. Type '---SAVE---' on a new line to save and exit.[/dim]"
        )
        console.print("[dim]Type '---CANCEL---' on a new line to cancel.[/dim]\n")

        if initial_content:
            console.print("[dim]Current content:[/dim]")
            console.print(Panel(initial_content, border_style="dim"))
            console.print(
                "\n[dim]Enter new content (will replace current content):[/dim]"
            )

        input_lines = []
        while True:
            try:
                line = input()
                if line.strip() == "---SAVE---":
                    break
                elif line.strip() == "---CANCEL---":
                    raise KeyboardInterrupt
                input_lines.append(line)
            except EOFError:
                break
            except KeyboardInterrupt:
                raise

        return "\n".join(input_lines)


def get_note_path(title: str, notebook: str = None) -> str:
    """Gets the full path for a note, optionally inside a notebook."""
    directory = os.path.join(NOTES_DIR, notebook) if notebook else NOTES_DIR
    if notebook:
        os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, f"{title}.md")


def find_note(title: str) -> str | None:
    """Finds a note by title across all notebooks."""
    for root, _, files in os.walk(NOTES_DIR):
        for file in files:
            if file == f"{title}.md":
                return os.path.join(root, file)
    return None


@app.command(help="Create a new note and edit it in the terminal.")
def new(
    title: str = typer.Argument(..., help="The title of the note."),
    notebook: str = typer.Option(
        None, "--notebook", "-n", help="Notebook to store the note in."
    ),
    template: str = typer.Option(
        None, "--template", "-t", help="Name of the template to use."
    ),
):
    note_path = get_note_path(title, notebook)
    if os.path.exists(note_path):
        console.print(
            f":warning: Note '[bold red]{title}.md[/bold red]' already exists."
        )
        if not typer.confirm("Do you want to edit the existing note?"):
            raise typer.Exit()

    # Start with title and basic structure
    initial_content = f"# {title.replace('-', ' ').title()}\n\n"

    if template:
        template_path = os.path.join(TEMPLATES_DIR, f"{template}.md")
        if os.path.exists(template_path):
            with open(template_path, "r", encoding="utf-8") as f:
                initial_content = f.read()
            console.print(f"Using template '[bold blue]{template}.md[/bold blue]'.")
        else:
            console.print(
                f":warning: Template '[bold red]{template}.md[/bold red]' not found."
            )
    elif os.path.exists(note_path):
        # Load existing content if editing
        with open(note_path, "r", encoding="utf-8") as f:
            initial_content = f.read()

    try:
        # Open the terminal editor
        content = terminal_editor(initial_content, f"Editing: {title}")

        # Save the note
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(content)

        console.print(
            f":sparkles: Saved note: '[bold green]{os.path.basename(note_path)}[/bold green]'"
        )
        console.print(f"[dim]Note saved to: {note_path}[/dim]")

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Note editing cancelled.[/bold yellow]")
        raise typer.Exit()


@app.command(help="Edit an existing note in the terminal.")
def edit(title: str = typer.Argument(..., help="The title of the note to edit.")):
    note_path = find_note(title)
    if not note_path:
        console.print(f":x: Note '[bold red]{title}.md[/bold red]' not found.")
        raise typer.Exit()

    # Load existing content
    with open(note_path, "r", encoding="utf-8") as f:
        initial_content = f.read()

    try:
        # Open the terminal editor
        content = terminal_editor(initial_content, f"Editing: {title}")

        # Save the note
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(content)

        console.print(
            f":sparkles: Saved note: '[bold green]{os.path.basename(note_path)}[/bold green]'"
        )
        console.print(f"[dim]Note saved to: {note_path}[/dim]")

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Note editing cancelled.[/bold yellow]")
        raise typer.Exit()


@app.command(help="List all available notes.")
def list():
    table = Table(title="My Notes 📚", show_header=True, header_style="bold magenta")
    table.add_column("Notebook", style="cyan")
    table.add_column("Note Title", style="green")

    notes_found = False
    for root, dirs, files in os.walk(NOTES_DIR):
        dirs.sort()
        files.sort()
        notebook_name = os.path.relpath(root, NOTES_DIR)
        if notebook_name == ".":
            notebook_name = "[Home]"

        for file in files:
            if file.endswith(".md"):
                notes_found = True
                table.add_row(notebook_name, file.replace(".md", ""))

    if not notes_found:
        console.print(
            "[bold yellow]No notes found. Create one with `notes new <title>`![/bold yellow]"
        )
        return

    console.print(table)


@app.command(help="Display the content of a note.")
def show(title: str = typer.Argument(..., help="The title of the note to show.")):
    note_path = find_note(title)
    if note_path:
        with open(note_path, "r") as f:
            content = Markdown(f.read(), style="default")
            panel = Panel(
                content, title=f"[bold cyan]{title}.md[/bold cyan]", border_style="blue"
            )
            console.print(panel)
    else:
        console.print(f":x: Note '[bold red]{title}.md[/bold red]' not found.")


@app.command(help="Delete a note.")
def delete(title: str = typer.Argument(..., help="The title of the note to delete.")):
    note_path = find_note(title)
    if note_path:
        os.remove(note_path)
        console.print(
            Panel(
                f"Deleted note '[bold red]{title}.md[/bold red]'.", border_style="red"
            )
        )
    else:
        console.print(f":x: Note '[bold red]{title}.md[/bold red]' not found.")


@app.command(help="Search for text within your notes.")
def search(query: str = typer.Argument(..., help="The text to search for.")):
    search_tool = "rg" if shutil.which("rg") else "grep"
    console.print(
        f"Searching for '[bold yellow]{query}[/bold yellow]' using {search_tool}..."
    )

    try:
        if search_tool == "rg":
            result = subprocess.run(
                [
                    search_tool,
                    "-i",
                    "--with-filename",
                    "--line-number",
                    query,
                    NOTES_DIR,
                ],
                capture_output=True,
                text=True,
            )
        else:
            result = subprocess.run(
                [search_tool, "-r", "-i", "-n", query, NOTES_DIR],
                capture_output=True,
                text=True,
            )

        if result.stdout:
            console.print(
                Panel(
                    result.stdout,
                    title="[bold green]Search Results[/bold green]",
                    border_style="green",
                )
            )
        else:
            console.print(
                Panel(
                    "No results found.",
                    title="[bold yellow]Search Results[/bold yellow]",
                    border_style="yellow",
                )
            )
    except Exception as e:
        console.print(f"[bold red]An error occurred during search: {e}[/bold red]")


@app.command(name="add", help="Quickly append text to your inbox.")
def append_to_inbox(text: str = typer.Argument(..., help="Text to append.")):
    inbox_path = get_note_path("inbox")
    with open(inbox_path, "a") as f:
        f.write(f"- {text}\n")
    console.print(f"Appended to '[bold green]inbox.md[/bold green]'.")


if __name__ == "__main__":
    app()
