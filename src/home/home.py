from flet import Page, Column, ElevatedButton, ListView, ListTile, Text

class HomeScreen:
    def __init__(self, page: Page):
        self.page = page
        self.build()

    def build(self):
        self.description = Text("Welcome to the app. You can upload and analyze images.")
        self.upload_button = ElevatedButton(text="Upload Image", on_click=self.go_upload)
        self.data_list = ListView(items=[])

        # ここで保存されたデータを取得し、リストに表示
        self.load_data()

        self.page.add(
            Column(
                controls=[
                    self.description,
                    self.upload_button,
                    self.data_list
                ]
            )
        )

    def go_upload(self, e):
        self.page.go("/upload")

    def load_data(self):
        # データベースからデータを取得し、self.data_listに追加
        pass
