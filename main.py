from flet import Page, app, colors, Column, Container, Row, IconButton, icons, web
import flet as ft
# from src.auth.login import LoginScreen
# from src.auth.register import RegisterScreen
# from src.auth.reset_password import ResetPasswordScreen
from src.home.home import HomeScreen
from src.upload.upload import UploadScreen
from src.results.results import ResultsScreen

def main(page: Page):
    page.title = "SnapMap"
    page.window.width = 375
    page.window.height = 812
    page.bgcolor = colors.GREY_300  # 背景色を設定
    page.margin = ft.margin.all(0)  # ページのマージンをゼロに設定
    page.padding = ft.padding.all(0)  # ページのパディングをゼロに設定

    # login_screen = LoginScreen(page)
    # register_screen = RegisterScreen(page)
    # reset_password_screen = ResetPasswordScreen(page)
    home_screen = HomeScreen()
    upload_screen = UploadScreen()
    results_screen = ResultsScreen()

    settings_button = IconButton(
        icon=ft.icons.SETTINGS,
        icon_size=24,
        icon_color=colors.GREY_600,
        hover_color=colors.BLUE_500,
        on_click=lambda e: page.go("/settings")
    )

    person_button = IconButton(
        icon=ft.icons.PERSON,
        icon_size=24,
        icon_color=colors.GREY_600,
        hover_color=colors.BLUE_500,
        on_click=lambda e: page.go("/profile")
    )

    home_button = IconButton(
        icon=ft.icons.HOME,
        icon_size=24,
        icon_color=colors.GREY_600,
        hover_color=colors.BLUE_500,
        on_click=lambda e: page.go("/home")
    )

    map_button = IconButton(
        icon=ft.icons.MAP,
        icon_size=24,
        icon_color=colors.GREY_600,
        hover_color=colors.BLUE_500,
        on_click=lambda e: page.go("/results")
    )

    list_button = IconButton(
        icon=ft.icons.LIST,
        icon_size=24,
        icon_color=colors.GREY_600,
        hover_color=colors.BLUE_500,
        on_click=lambda e: page.go("/results")
    )

    # ヘッダー
    header = ft.Container(
        ft.Row(
            [
                ft.Text("Snapmap DemoApp", size=20),
                ft.Row(
                    [
                        settings_button,
                        person_button,
                    ],
                    alignment="end"
                )
            ],
            alignment="spaceBetween"
        ),
        padding=ft.padding.all(10),
        bgcolor=ft.colors.WHITE,
        margin=ft.margin.all(0),
        width=page.window.width,
        height=50,
        # shadow=ft.BoxShadow(
        #     offset=ft.Offset(0, 2),
        #     blur_radius=5,
        #     spread_radius=1,
        #     color=ft.colors.with_opacity(ft.colors.BLACK, 0.2)
        # )
    )

    # フッター
    footer = ft.Container(
        ft.Row(
            [
                home_button,
                map_button,
                list_button
            ],
            alignment="spaceAround"
        ),
        padding=ft.padding.all(10),
        bgcolor=ft.colors.WHITE,
        margin=ft.margin.all(0),
        width=page.window.width,
        height=50,
        # shadow=ft.BoxShadow(
        #     offset=ft.Offset(0, -2),
        #     blur_radius=5,
        #     spread_radius=1,
        #     color=ft.colors.with_opacity(ft.colors.BLACK, 0.2)
        # )
    )

    content_container = Container(
        expand=True, margin=ft.margin.all(10), padding=ft.padding.all(15), bgcolor=ft.colors.WHITE
    )  # ページコンテンツ用のコンテナ

    page.add(
        Column(
            controls=[
                header,  # ヘッダー
                content_container,  # コンテンツを保持するコンテナ
                footer  # フッター
            ],
            expand=True,
            tight=True,
            spacing=10,  # 列のスペーシングをゼロに設定
            alignment="spaceBetween"  # ヘッダーとフッターを上下に配置
        ),
    )

    def route_change(handler):
        print(f"[DEBUG] Route changed to: {handler.route}")
        content_container.content = None  # 既存のコンテンツをクリア
        # if route == "/login":
        #     login_screen.build(content_container)
        # elif route == "/register":
        #     register_screen.build(content_container)
        # elif route == "/reset_password":
        #     reset_password_screen.build(content_container)
        route = handler.route
        if route.startswith("/home"):
            home_screen.build(content_container)
        elif route.startswith("/upload"):
            upload_screen.build(content_container)
        elif route.startswith("/results"):
            results_screen.build(content_container)

        page.update()

    page.on_route_change = route_change

    # 初期画面
    print('Going to home')
    page.go("/home")

if __name__ == "__main__":
    app(target=main, host="0.0.0.0")
