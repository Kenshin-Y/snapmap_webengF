from flet import Container, Column, ElevatedButton, ListView, ListTile, Text, colors

class HomeScreen:
    def __init__(self):
        self.container = None

    def build(self, container: Container):
        print("HomeScreen.build")
        self.container = container
        self.description = Text(
            "Results List",
            color=colors.BLACK,
            size=16,
            text_align="center"
        )
        self.upload_button = ElevatedButton(
            text="Upload Image",
            on_click=self.go_upload,
            bgcolor=colors.BLUE_500,
            color=colors.WHITE,
            height=50,
            width=200,
        )
        self.data_list = ListView(
            height=300,
            controls=[]
        )

        # ここで保存されたデータを取得し、リストに表示
        self.load_data()

        container.content = Column(
            controls=[
                self.description,
                self.upload_button,
                self.data_list,
            ],
            spacing=20,
            alignment="start",  # コンテンツを上詰めに配置
            expand=False  # Columnを縦に広げる
        )
        container.update()

    def go_upload(self, e):
        self.container.page.go("/upload")

    def load_data(self):
        # データベースからデータを取得し、self.data_listに追加
        # ここではサンプルデータを追加します
        sample_data = [f'Data {i}' for i in range(1, 11)]
        for item in sample_data:
            self.data_list.controls.append(
                ListTile(
                    title=Text(item, color=colors.BLACK),
                    on_click=lambda e, item=item: self.view_details(item)
                )
            )

    def view_details(self, item):
        # データ詳細表示画面に遷移
        self.container.page.go(f"/details/{item}")
