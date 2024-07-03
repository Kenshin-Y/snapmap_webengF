import json
import requests


def get_hotpepper_apikey():
    with open("secret.json") as f:
        secret = json.load(f)
    return secret["HOTPEPPER_API_KEY"]


def verify_hotpepper(output: dict) -> str:
    # ここにhotpepperAPIを使って、説明文の内容を検証する処理を書く.
    try:
        HOTPEPPER_API_KEY = get_hotpepper_apikey()
        # 検索キーワードを設定
        url = f'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key={HOTPEPPER_API_KEY}&format=json'
        kwd = ""
        for k in ["name", "address", "tel"]:
            if k in output.keys() and output[k] != "" and k+"_probability" in output.keys() and output[k+"_probability"] > 0.5:
                kwd += output[k] + " "
        url += f"&keyword={kwd}"

        response = requests.get(url)
        response_json = response.json()['results']

        if "results_available" in response_json.keys() and response_json['results_available'] > 0:
            verification_status = f"""
            Hotpepper上に存在する店舗です．\n
            {response_json}\n
            該当件数：{response_json['results_available']}件\n
            """
            for i, shop in enumerate(response_json['shop']):
                verification_status += f"""
                {i+1}件目\n
                \t店名: {shop['name']}\n
                \t住所: {shop['address']}\n
                \tURL: {shop['urls']}\n
                """
        else:
            verification_status = "Hotpepper上に存在しない店舗です．" 

    except Exception as e:
        verification_status = f"検証時エラー: 開発者に問い合わせください．\n{e}"

    return verification_status