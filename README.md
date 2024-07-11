# グループF_新しい地図アプリ

完全な機能を提供するには，APIKEYを取得して`secret.json`を作成します．
```
{
    "OPENAI_API_KEY": "XXX",
    "HOTPEPPER_API_KEY": "XXX",
    "GOOGLEMAP_API_KEY": "XXX"
}
```

Windowsコマンドプロンプトで以下を実行します．
(WSLだと画像選択を行うためにXwindowを使う必要があります)
```
$ pip install -r requirements.txt
$ flet run ./
```

註: ` pip freeze > .\requirements.txt` しただけなのでいろいろ混ざってます
