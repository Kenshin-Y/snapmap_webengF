import flet as ft
import json
import sqlite3

class ListViewScreen(ft.UserControl):

    def __init__(self):
        super().__init__()
        self.title = "ListView"

    def build(self, container: ft.Container):
        self.container = container
        self.container.content = self._build_content()
        self.container.update()
    
    def _build_content(self):
        # results.dbからデータを取得
        conn = sqlite3.connect('results.db')
        c = conn.cursor()
        c.execute("SELECT result_json, latitude, longitude FROM results")
        results = c.fetchall()
        conn.close()

        # データを表示するためのリストアイテムを作成
        list_items = [
            ft.Text("Database Results", size=20, weight="bold", color=ft.colors.BLACK, text_align="center"),
        ]
        for result in results:
            result_json = json.loads(result[0])
            latitude = result[1]
            longitude = result[2]
            list_items.append(
                ft.Container(content=
                    ft.Column(controls=[
                        # お店の名前と位置情報を表示
                        ft.Text(f"Name: {result_json.get('name', 'N/A')}", weight="bold"),
                        ft.Text(f"Discription: {result_json.get('description', 'N/A')}"),
                        ft.Text(f"Lat: {latitude}, Lng: {longitude}")
                    ]),
                    bgcolor=ft.colors.GREY_300,
                )
            )

        # リストビューを作成
        list_view = ft.ListView(
            controls=list_items,
            expand=True,
            spacing=20
        )

        return list_view
