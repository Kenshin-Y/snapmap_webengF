from flet import Page, Column, TextField, ElevatedButton, Text

class LoginScreen:
    def __init__(self, page: Page):
        self.page = page
        self.build()

    def build(self):
        self.email = TextField(label="Email")
        self.password = TextField(label="Password", password=True)
        self.login_button = ElevatedButton(text="Login", on_click=self.login)
        self.register_link = Text("Register", on_click=self.go_register)
        self.reset_link = Text("Reset Password", on_click=self.go_reset_password)

        self.page.add(
            Column(
                controls=[
                    self.email,
                    self.password,
                    self.login_button,
                    self.register_link,
                    self.reset_link
                ]
            )
        )

    def login(self, e):
        # ログインロジックを実装
        pass

    def go_register(self, e):
        self.page.go("/register")

    def go_reset_password(self, e):
        self.page.go("/reset_password")
