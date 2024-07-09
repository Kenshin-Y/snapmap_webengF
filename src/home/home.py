import flet as ft

class HomeScreen(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.title = "Home"

    def build(self, container: ft.Container):
        self.container = container
        self.container.content = self._build_content()
        self.container.update()

    def _build_content(self):
        return ft.ListView(
            controls=[
                ft.Container(content=
                    ft.Row(controls=[
                            ft.Image(src="assets/main_bg.png", fit="cover", height=812//3, width=375//3),
                            ft.Text("新しい地図アプリ\nSnapmap", size=24, weight="bold", color=ft.colors.PURPLE_900)
                        ],
                        spacing=10,
                    ),
                ),
                # 今すぐ登録のボタン
                ft.ElevatedButton(
                    text="[DEMO] 今すぐ登録する",
                    bgcolor=ft.colors.PURPLE_700,
                    color=ft.colors.WHITE,
                    height=50,
                    width=100,
                    on_click=self.go_upload
                ),

                # Features Section
                ft.Container(
                    content=ft.Column(controls=[
                        ft.Text("特徴", size=28, weight="bold", color=ft.colors.PURPLE_900),
                        ft.Column(controls=[
                            ft.Icon(name=ft.icons.SCREENSHOT, size=48, color=ft.colors.PURPLE_700),
                            ft.Text("AIによる解析", size=16, weight="bold"),
                            ft.Text("AIがあなたのスクリーンショットを解析し，お店の位置情報を自動で検出します．"),
                        ], spacing=10, horizontal_alignment="center",),
                        ft.Column(controls=[
                            ft.Icon(name=ft.icons.MAP, size=48, color=ft.colors.PURPLE_700),
                            ft.Text("自動でマップに保存", size=16, weight="bold"),
                            ft.Text("気になるお店のスクリーンショットを自動解析して位置情報を取得し，マップ上に保存．あなたのカメラロールをマップに．"),
                        ], spacing=10, horizontal_alignment="center",),  
                        ft.Column(controls=[    
                            ft.Icon(name=ft.icons.PEOPLE_ALT, size=48, color=ft.colors.PURPLE_700),
                            ft.Text("お店をシェア", size=16, weight="bold"),
                            ft.Text("友達機能を使って，あなたが保存したお店を家族・友達・恋人と共有することができます．"),
                        ], spacing=10, horizontal_alignment="center",),  
                    ],
                    spacing=50,
                    horizontal_alignment="center",
                    )
                ),
                # 今すぐ登録のボタン
                ft.ElevatedButton(
                    text="[DEMO] 今すぐ登録する",
                    bgcolor=ft.colors.PURPLE_700,
                    color=ft.colors.WHITE,
                    height=50,
                    width=100,
                    on_click=self.go_upload
                ),

                # 空白
                ft.Container(height=20),
                # CopyRight Section
                ft.Container(
                    content=ft.Column(controls=[
                        ft.Text("© 2021 Snapmap\nAll Rights Reserved\nDeveloped by Flet", size=12, color=ft.colors.GREY_600),
                        ],
                        horizontal_alignment="center",
                    ),
                ),
            ],
            spacing=20,
        )

    def go_upload(self, e):
        self.container.page.go(route=f'/upload')


def main(page: ft.Page):
    page.title = "Snapmap DemoApp"
    page.add(HomeScreen())


if __name__ == "__main__":
    ft.app(target=main)
