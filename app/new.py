import sys

from rich.syntax import Syntax
from rich.traceback import Traceback

from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.reactive import var
from textual.widgets import DirectoryTree, Footer, Header, TextArea

import os

class CodeBrowser(App):
    """Textual code browser app."""

    CSS_PATH = "./css/code_browser.tcss"
    BINDINGS = [
        ("f", "toggle_files", "Toggle Files"),
        ("q", "quit", "Quit"),
    ]

    show_tree = var(True)

    def watch_show_tree(self, show_tree: bool) -> None:
        """Called when show_tree is modified."""
        self.set_class(show_tree, "-show-tree")

    def compose(self) -> ComposeResult:
        """Compose our UI."""
        path = "./" if len(sys.argv) < 2 else sys.argv[1]
        yield Header()
        with Container():
            yield DirectoryTree(path, id="tree-view")
            with VerticalScroll(id="code-view"):
                yield TextArea("This is a test!", id="code" )
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(DirectoryTree).focus()

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        """Called when the user click a file in the directory tree."""
        event.stop()
        code_view = self.query_one("#code", TextArea)
        self.load_file_edit_area(event.path, "#code")
        try:
            # with open(event.path, "r") as file:
            #     content = file.read()
            #     print(content)
            #     code_view = self.query_one("#code", TextArea)
            #     code_view.load_text(content)
            #     self.sub_title = str(event.path)
           pass 
           # self.load_file_edit_area(event.path, "#code"
        except Exception:
            code_view.value = f"Error reading file: {event.path}"
            self.sub_title = "ERROR"

    def action_toggle_files(self) -> None:
        """Called in response to key binding."""
        self.show_tree = not self.show_tree
    
    def load_file_edit_area(self, filepath, textarea_id) -> None:
        fileext = os.path.splitext(filepath)
        lang_options = {
            "py": "python",
            "java": "java",
            "js": "javascript",
            "md": "markdown",
        }
        try:
            file_lang = lang_options[fileext[1].replace(".","")]
        except KeyError:
            file_lang = None
        
        code_buff = self.query_one(textarea_id, TextArea)
        print("test")
        with open(filepath, 'r') as file:
            file_content = file.read()
            code_buff.theme = "dracula"
            code_buff.language = file_lang
            code_buff.load_text(file_content)
            print(file_lang)
            print(code_buff)
            



if __name__ == "__main__":
    CodeBrowser().run()
