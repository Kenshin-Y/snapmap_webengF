import flet as ft
import folium
import json
import sqlite3
from folium.plugins import MarkerCluster

class MapViewScreen:
    def __init__(self):
        self.container = None

    def build(self, container: ft.Container):
        self.container = container
        self.display_map(container)

    def display_map(self, container):
        # データベースからデータを取得
        conn = sqlite3.connect('results.db')
        c = conn.cursor()
        c.execute("SELECT result_json, latitude, longitude FROM results")
        results = c.fetchall()
        conn.close()

        # Foliumを使用してマップを作成
        m = folium.Map(location=[35.6895, 139.6917], zoom_start=10)  # 東京の中心
        marker_cluster = MarkerCluster().add_to(m)

        for result in results:
            result_json = json.loads(result[0])
            latitude = result[1]
            longitude = result[2]
            folium.Marker(
                location=[latitude, longitude],
                popup=json.dumps(result_json, indent=2, ensure_ascii=False)
            ).add_to(marker_cluster)

        # マップをHTMLファイルとして保存
        m.save('map.html')
            
        # Fletで表示
        container.content = ft.Column([
            ft.Text("Map View", size=20, weight="bold", color=ft.colors.BLACK, text_align="center"),
            ft.WebView('map.html')
        ], spacing=20)
        container.update()
