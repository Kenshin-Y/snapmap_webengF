from flet import Page, Column, TextField, ElevatedButton, Text

class RegisterScreen:
    def __init__(self, page: Page):
        self.page = page
        self.build()

    def build(self):
        self.username = TextField(label="Username")
        self.email = TextField(label="Email")
        self.password = TextField(label="Password", password=True)
        self.confirm_password = TextField(label="Confirm Password", password=True)
        self.register_button = ElevatedButton(text="Register", on_click=self.register)
        self.login_link = Text("Login", on_click=self.go_login)

        self.page.add(
            Column(
                controls=[
                    self.username,
                    self.email,
                    self.password,
                    self.confirm_password,
                    self.register_button,
                    self.login_link
                ]
            )
        )

    def register(self, e):
        # 登録ロジックを実装
        pass

    def go_login(self, e):
        self.page.go("/login")
