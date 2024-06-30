from flet import Page, Column, ElevatedButton, Text

class ResultsScreen:
    def __init__(self, page: Page):
        self.page = page
        self.build()

    def build(self):
        self.results_text = Text("Analysis results will be displayed here.")
        self.save_button = ElevatedButton(text="Save to Database", on_click=self.save_results)
        self.back_button = ElevatedButton(text="Back to Home", on_click=self.go_home)

        self.page.add(
            Column(
                controls=[
                    self.results_text,
                    self.save_button,
                    self.back_button
                ]
            )
        )

    def save_results(self, e):
        # 解析結果をデータベースに保存するロジックを実装
        pass

    def go_home(self, e):
        self.page.go("/home")
