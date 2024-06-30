from flet import Page, Column, ElevatedButton, FilePicker, Image

class UploadScreen:
    def __init__(self, page: Page):
        self.page = page
        self.build()

    def build(self):
        self.file_picker = FilePicker(on_change=self.file_selected)
        self.image_preview = Image()
        self.analyze_button = ElevatedButton(text="Analyze Image", on_click=self.analyze, disabled=True)

        self.page.add(
            Column(
                controls=[
                    self.file_picker,
                    self.image_preview,
                    self.analyze_button
                ]
            )
        )

    def file_selected(self, e):
        if self.file_picker.value:
            self.image_preview.src = self.file_picker.value
            self.analyze_button.disabled = False

    def analyze(self, e):
        # 画像解析ロジックを実装
        pass
