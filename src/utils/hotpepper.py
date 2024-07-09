import json
import requests


def get_hotpepper_apikey():
    with open("secret.json") as f:
        secret = json.load(f)
    return secret["HOTPEPPER_API_KEY"]


def verify_hotpepper(output: dict) -> dict:
    # ここにhotpepperAPIを使って、説明文の内容を検証する処理を書く.
    try:
        api_key = get_hotpepper_apikey()
        print('[DEBUG]: ',api_key)
        # 検索キーワードを設定
        url = f'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key={api_key}&format=json'
        kwd = ""
        for k in ["name", "address", "tel"]:
            if k in output.keys() and output[k] != "" and k+"_probability" in output.keys() and output[k+"_probability"] > 0.5:
                kwd += output[k] + " "
        url += f"&keyword={kwd}"

        print(f'[DEBUG]: {url}')
        response = requests.get(url)
        response_json = response.json()['results']

        if "results_available" in response_json.keys() and response_json['results_available'] > 0:
            return response_json
        else:
            return {"error": "Hotpepper上に存在しない店舗です." }

    except Exception as e:
        return {"error": f"検証時エラー: 開発者に問い合わせください．{e}"}

    return {}