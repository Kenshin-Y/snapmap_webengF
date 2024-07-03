from flet import Container, Column, Row, ElevatedButton, Text, colors, Image, ListView
import json
import sys


from flet import UserControl

class JSONViewer(UserControl):
    def __init__(self, json_data):
        super().__init__()
        self.json_data = json_data

    def build(self):
        json_text = json.dumps(self.json_data, indent=2, ensure_ascii=False)
        return Text(
            json_text,
            color=colors.BLACK,
            size=16,
            text_align="left",
            selectable=True
        )


class ResultsScreen:
    """
    解析結果画面
    """
    def __init__(self):
        self.container = None

        self.save_button = ElevatedButton(
            text="Save Database",
            on_click=self.save_results,
            bgcolor=colors.GREEN_500,
            color=colors.WHITE,
            height=50,
            width=150
        )

        self.back_button = ElevatedButton(
            text="Back to Home",
            on_click=self.go_home,
            bgcolor=colors.BLUE_500,
            color=colors.WHITE,
            height=50,
            width=150
        )

    def build(self, container: Container):
        print("ResultsScreen.build")
        self.container = container
        route = container.page.route
        params = route.split("?")[1] if "?" in route else ""
        param_dict = dict(p.split("=") for p in params.split("&")) if params else {}
        print(f'param_dict: {param_dict}')

        result_json = param_dict.get("result_json").replace("'",'"')
        verification_str = param_dict.get("verifycation_str")
        image_path = param_dict.get("image_path")

        try:
            result_data = json.loads(result_json) if result_json else {}
            print(f'result_data: {result_data}')
        except json.JSONDecodeError:
            print("JSON Decode Error")
            result_data = {}
        self.result_json_viewer = JSONViewer(result_data)

        scrollable_content = ListView(
            controls=[
                Text(
                    "Analysis Result",
                    color=colors.BLACK,
                    size=20,
                    weight="bold",
                    text_align="center"
                ),
                self.result_json_viewer,
                Text(
                    "Verification Result",
                    color=colors.BLACK,
                    size=20,
                    weight="bold",
                    text_align="center"
                ),
                Text(
                    value=verification_str,
                    color=colors.BLACK,
                    size=16,
                    text_align="left"
                ),
                Image(src=image_path, fit="contain"),
                Row([
                    self.back_button,
                    self.save_button,
                ]),
            ],
            adaptive=True,
        )
        container.content = scrollable_content
        container.update()

    def save_results(self, e):
        # 解析結果をデータベースに保存するロジックを実装
        pass

    def go_home(self, e):
        self.container.page.go("/home")
