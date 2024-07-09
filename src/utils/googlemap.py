import requests
import json


def get_googlemap_apikey():
    with open("secret.json") as f:
        secret = json.load(f)
    return secret["GOOGLEMAP_API_KEY"]


def verify_googlemap(output: dict) -> dict:
    try:
        api_key = get_googlemap_apikey()
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

        # 信頼度の高い情報のみ検索クエリに追加 うまくいかないので一旦コメントアウト
        # query = ""
        # for k in ["name", "tel", "address", "genre"]:
        #     if output[f'{k}_probability'] > 0.5:
        #         query += output[k] + " "
        params = {
            "query": output['name'],
            "key": api_key,
            "fields": "name,formatted_address,geometry",
        }
        response = requests.get(base_url, params=params)
        res = response.json()
        # name, formatted_address, geometryのみ取得
        result = {
            'formatted_address': res['results'][0]['formatted_address'],
            'lat': res['results'][0]['geometry']['location']['lat'],
            'lng': res['results'][0]['geometry']['location']['lng'],
            'name': res['results'][0]['name'],
        }
 
        if response.status_code == 200:     
            return result
        else:
            return {"error": "Google Map での検索結果が取得できませんでした．"}

    except Exception as e:
        return {"error": "検証時エラー: 開発者に問い合わせください．{e}"}
