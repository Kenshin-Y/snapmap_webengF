import flet as ft
import os, sys
from PIL import Image

from src.utils.gpt4 import gen_chat_response_with_gpt4


class UploadScreen:
    def __init__(self):
        self.file_picker = ft.FilePicker(on_result=self.file_selected)
        self.image_preview = ft.Container(
            ft.Text("画像をアップロード", size=16, color=ft.colors.GREY_600),
            bgcolor=ft.colors.GREY_200,
            alignment=ft.alignment.center
        )
        self.selected_image_path = None
        self.select_button = ft.ElevatedButton(
            text="画像を選択",
            on_click=self.pick_files,
            bgcolor=ft.colors.BLUE_500,
            color=ft.colors.WHITE,
            height=50,
            width=150
        )
        self.analyze_button = ft.ElevatedButton(
            text="解析開始",
            on_click=self.analyze,
            disabled=True,
            bgcolor=ft.colors.GREEN_500,
            color=ft.colors.WHITE,
            height=50,
            width=150
        )

    def build(self, container: ft.Container):
        self.container = container
        self.selected_image_path = None
        self.loading_indicator = ft.ProgressBar(visible=False)
        self.image_preview.src = None
        self.analyze_button.disabled = True

        container.content = ft.Column(
            [
                self.file_picker,
                ft.Text("画像アップロード", size=20, weight="bold", color=ft.colors.BLACK),
                ft.Row([
                    self.select_button,
                    self.analyze_button,
                ], alignment="center", spacing=10),
                self.loading_indicator,
                ft.Container(
                    self.image_preview,
                    padding=ft.padding.all(10),
                    bgcolor=ft.colors.GREY_200,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
            spacing=10,
            alignment="start",  # コンテンツを上詰めに配置
            expand=False  # Columnを縦に広げる
        )
        container.update()

    def pick_files(self, e):
        self.file_picker.pick_files(allow_multiple=False)

    def file_selected(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.selected_image_path = e.files[0].path
            self.image_preview.content = ft.Image(src=e.files[0].path, fit="contain")
            self.analyze_button.disabled = False
            self.image_preview.update()
            self.container.page.update()

    def analyze(self, e):
        # 解析を行って，結果のJSONを保存する
        self.loading_indicator.visible = True
        self.container.update()
        image = Image.open(self.selected_image_path)
        result_json, verifycation_str = gen_chat_response_with_gpt4(image)
        self.loading_indicator.visible = False

        # 結果画面に遷移
        self.container.page.go(route=f'/results?result_json={result_json}&verifycation_str={verifycation_str}&image_path={self.selected_image_path}')
