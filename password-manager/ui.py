from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Header, Footer, Input, Static
from textual.screen import Screen

class CreateAccount(Screen):
    def compose(self) -> ComposeResult:
        yield Static('Create an Account')
        yield Input(
            placeholder="Enter your email...",
        )
        yield Input(
            placeholder="Enter your password...",
        )
        yield Button("Create")

class Login(Screen):
    def compose(self) -> ComposeResult:
        yield Static('Login Screen')
        yield Input(
            placeholder="Enter your email...",
        )
        yield Input(
            placeholder="Enter your password...",
        )
        yield Button("Login")
        yield Button('Dont have an Account? Create one')


class PasswordManagerApp(App):
    BINDINGS = [
        ('q', 'quit', 'Quit Program'),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Login()
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case 'quit':
                self.exit()
