import requests
import json


def get_googlemap_apikey():
    with open("secret.json") as f:
        secret = json.load(f)
    return secret["GOOGLEMAP_API_KEY"]


def verify_googlemap(output: dict) -> str:
    try:
        api_key = get_googlemap_apikey()
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

        # 信頼度の高い情報のみ検索クエリに追加
        query = ""
        for k in ["name", "tel", "address", "genre"]:
            if output[f'{k}_probability'] > 0.5:
                query += output[k] + " "
        params = {
            "query": output['name'],
            "key": api_key,
            "fields": "name,formatted_address",
        }
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            result = json.format(response.json(), indent=2, ensure_ascii=False)
            verification_status = f"""
            Google Map での検索結果:\n
            {result}
            """        
            return verification_status
        else:
            return "Google Map での検索結果が取得できませんでした．"

    except Exception as e:
        return "検証時エラー: 開発者に問い合わせください．\n{e}"
