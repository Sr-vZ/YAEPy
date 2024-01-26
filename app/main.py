# # import textual as tx
# # from textual.app import App
# # from textual.scroll_view import ScrollView

# # # from widgets import Editor, FileBrowser
# # from widgets.editor import Editor
# # from widgets.file_browser import FileBrowser


# # class YAEPYApp(App):
# #     async def on_mount(self) -> None:
# #         await self.view.dock(FileBrowser(), edge="left", size=30)
# #         await self.view.dock(ScrollView(Editor()), edge="top")

# # if __name__ == "__main__":
# #     app = CodeEditorApp()
# #     app.run()

# from textual.app import App, ComposeResult
# from textual.screen import Screen
# from textual.widgets import Placeholder


# class Header(Placeholder):
#     DEFAULT_CSS = """
#     Header {
#         height: 1;
#         dock: top;
#     }
#     """


# class Footer(Placeholder):
#     DEFAULT_CSS = """
#     Footer {
#         height: 1;
#         dock: bottom;
#     }
#     """


# class ColumnsContainer(Placeholder):
#     DEFAULT_CSS = """
#     ColumnsContainer {
#         width: 1fr;
#         height: 1fr;
#         border: solid white;
#     }
#     """  


# class TweetScreen(Screen):
#     def compose(self) -> ComposeResult:
#         yield Header(id="Header")
#         yield Footer(id="Footer")
#         yield ColumnsContainer(id="Columns")


# class YAEPYApp(App):
#     def on_ready(self) -> None:
#         self.push_screen(TweetScreen())


# if __name__ == "__main__":
#     app = YAEPYApp()
#     app.run()

"""
Code browser example.

Run with:

    python code_browser.py PATH
"""

import sys

from rich.syntax import Syntax
from rich.traceback import Traceback

from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.reactive import var
from textual.widgets import DirectoryTree, Footer, Header, Static, TextArea
from textual.widgets.text_area import TextAreaTheme

class CodeBrowser(App):
    """Textual code browser app."""

    CSS_PATH = "./css/code_browser.tcss"
    BINDINGS = [
        ("f", "toggle_files", "Toggle Files"),
        ("q", "quit", "Quit"),
    ]

    show_tree = var(True)

    
    def load_file_content(self, file_path):
        # Load the content of the selected file into the TextArea
        try:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.value = content
        except FileNotFoundError:
            self.text_area.value = f"File not found: {file_path}"

    
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
                # yield Static(id="code", expand=True)
                # yield TextArea(id="code", text)
                code_area = TextArea("TEXT", id="code")
                yield code_area
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(DirectoryTree).focus()

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        """Called when the user click a file in the directory tree."""
        event.stop()
        code_view = self.query_one("#code", TextArea)
        with open(event.path,'r') as f:
            content = f.read()
            print(content)
            code_view.value = "content"
        try:
            syntax = Syntax.from_path(
                str(event.path),
                line_numbers=True,
                word_wrap=False,
                indent_guides=True,
                # theme="github-dark",
            )
        except Exception:
            code_view.update(Traceback(theme="github-dark", width=None))
            self.sub_title = "ERROR"
        else:
            # code_view.update(syntax)
            # load_file_content(event.path)
            with open(event.path,'r') as f:
                content = f.read()
                print(content)
                code_view.value = content
            # self.query_one("#code-view").scroll_home(animate=False)
            self.sub_title = str(event.path)

    def action_toggle_files(self) -> None:
        """Called in response to key binding."""
        self.show_tree = not self.show_tree
    

if __name__ == "__main__":
    CodeBrowser().run()