import flet as ft
import json
import sys
import sqlite3


class JSONViewer(ft.UserControl):
    def __init__(self, json_data):
        super().__init__()
        self.json_data = json_data

    def build(self):
        json_text = json.dumps(self.json_data, indent=2, ensure_ascii=False)
        return ft.Text(
            json_text,
            color=ft.colors.BLACK,
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

        self.save_button = ft.ElevatedButton(
            text="保存",
            on_click=self.save_results,
            bgcolor=ft.colors.GREEN_500,
            color=ft.colors.WHITE,
            height=50,
            width=150
        )

        self.back_button = ft.ElevatedButton(
            text="ホームに戻る",
            on_click=self.go_home,
            bgcolor=ft.colors.BLUE_500,
            color=ft.colors.WHITE,
            height=50,
            width=150
        )

    def build(self, container: ft.Container):
        print("ResultsScreen.build")
        self.container = container
        route = container.page.route
        params = route.split("?")[1] if "?" in route else ""
        print(f'params: {params}')
        param_dict = dict(p.split("=") for p in params.split("&")) if params else {}
        print(f'param_dict: {param_dict}')

        result_json = param_dict.get("result_json").replace("'",'"')
        verification_hp = param_dict.get("verifycation_hp").replace("'",'"')
        verification_gm = param_dict.get("verifycation_gm").replace("'",'"')

        # # str to dict
        # result_json = json.loads(result_json) if result_json else {}
        # verification_hp = json.loads(verification_hp) if verification_hp else {}
        # verification_gm = json.loads(verification_gm) if verification_gm else {}
    
        image_path = param_dict.get("image_path")

        try:
            result_json = json.loads(result_json) if result_json else {}
            print(f'result_json: {result_json}')
        except json.JSONDecodeError:
            print("JSON Decode Error")
        
        try:
            verification_hp = json.loads(verification_hp) if verification_hp else {}
            print(f'verification_hp: {verification_hp}')
        except json.JSONDecodeError:
            print("JSON Decode Error")

        try:
            verification_gm = json.loads(verification_gm) if verification_gm else {}
            print(f'verification_gm: {verification_gm}')
        except json.JSONDecodeError:
            print("JSON Decode Error")

        self.result_json_viewer = JSONViewer(result_json)
        self.verifycation_hp_viewer = JSONViewer(verification_hp)
        self.verifycation_gm_viewer = JSONViewer(verification_gm)

        scrollable_content = ft.ListView(
            controls=[
                ft.Text("解析結果", color=ft.colors.BLACK, size=20, weight="bold", text_align="center"),
                ft.Container(
                    self.result_json_viewer,
                    padding=ft.padding.all(10),
                    bgcolor=ft.colors.GREY_200,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.Text("[DEMO] Verify結果\nhotpepper API", color=ft.colors.BLACK, size=20, weight="bold", text_align="center"),
                ft.Container(
                    self.verifycation_hp_viewer,
                    padding=ft.padding.all(10),
                    bgcolor=ft.colors.GREY_200,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.Text("[DEMO] Verify結果\ngooglemap API", color=ft.colors.BLACK, size=20, weight="bold", text_align="center"),
                ft.Container(
                    self.verifycation_gm_viewer,
                    padding=ft.padding.all(10),
                    bgcolor=ft.colors.GREY_200,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.Row([
                    self.back_button,
                    self.save_button,
                ]),
                ft.Image(src=image_path, fit="contain"),
            ],
            adaptive=True,
            spacing=20,
        )
        container.content = scrollable_content
        container.update()

    def save_results(self, e):
        """
        verification_gmのデータを取得してデータベースに保存
        """
        print("Saving results to database")
        route = self.container.page.route
        params = route.split("?")[1] if "?" in route else ""
        param_dict = dict(p.split("=") for p in params.split("&")) if params else {}

        result_json = param_dict.get("result_json").replace("'", '"')
        verification_gm = param_dict.get("verifycation_gm").replace("'", '"')

        try:
            result_json = json.loads(result_json)
        except json.JSONDecodeError:
            print("JSON Decode Error")
            result_json = {}

        try:
            verification_gm_data = json.loads(verification_gm) 
            latitude = verification_gm_data['lat']
            longitude = verification_gm_data['lng']
        except json.JSONDecodeError:
            print("JSON Decode Error")
            latitude = None
            longitude = None

        if latitude and longitude:
            self.save_result_to_db(result_json, latitude, longitude)
        else:
            print("Latitude or Longitude is missing in verification_gm")

    def save_result_to_db(self, result_json, latitude, longitude):
        print(f"Results saving to database: {result_json}, {latitude}, {longitude}")
        conn = sqlite3.connect('results.db')
        c = conn.cursor()
        c.execute("INSERT INTO results (result_json, latitude, longitude) VALUES (?, ?, ?)",
                  (json.dumps(result_json), latitude, longitude))
        conn.commit()
        conn.close()
        print(f"Finish saving to db.")

    def go_home(self, e):
        self.container.page.go("/home")
