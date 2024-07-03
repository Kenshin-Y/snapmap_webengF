import base64
import io
import requests
import json
import re
from typing import Tuple, Dict
from PIL import Image
from openai import OpenAI, APIConnectionError


SYSTEM_ROLE_CONTENT = \
    """
    あなたは画像から読み取れる店舗の情報を検索し，保存しようとしています．\n
    ブラウザ検索を行って，最新の情報を取得してください．\n
    """

PROMPT_TEMPLATE = \
    """
    添付した画像から店舗の情報を取得し，情報の内容とその確信度を以下の形式で出力してください．\n
    json形式は以下のようになっています．\n
    取得できなかった情報は空欄としてください．\n
    ```json
    {
        "name": "店名",
        "name_probability": 0.92,
        "address": "東京都文京区本郷1-1",
        "address_probability": 0.74,
        "tel": "00000000000",
        "tel_probability": 0.21,
        "genre": "居酒屋",
        "genre_probability": 0.99,
        "description": "最高級A5ランク和牛を使ったステーキで有名な鉄板焼きレストランです。"
        "description_probability": 0.85
    }
    ```
    """


def get_gpt_openai_apikey():
    with open("secret.json") as f:
        secret = json.load(f)
    return secret["OPENAI_API_KEY"]


def get_hotpepper_apikey():
    with open("secret.json") as f:
        secret = json.load(f)
    return secret["HOTPEPPER_API_KEY"]


def encode_image(image):
    byte_arr = io.BytesIO()
    image.save(byte_arr, format='JPEG')
    base64_image = f"data:image/jpeg;base64,{base64.b64encode(byte_arr.getvalue()).decode()}"
    return base64_image


def create_message(system_role, prompt, image_base64):
    """
    create message for GPT-4o
    """
    message = [
        {
            'role': 'system',
            'content': system_role
        },
        {
            'role': 'user',
            'content': [
                {
                    'type': 'text',
                    'text': prompt
                },
                {
                    'type': 'image_url',
                    'image_url': {
                        'url': image_base64
                    }
                },
            ]
        },
    ]
    return message


def verify_googlemap(output: dict) -> str:
    pass


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


def verify_output(output: dict) -> str:
    """
    Verify the description with another API or logic
    """
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


def gen_chat_response_with_gpt4(image: Image) -> Tuple[Dict, str]:
    """
    generate chat response with GPT-4o
    """
    openai_client = OpenAI(api_key=get_gpt_openai_apikey())
    image_base64 = encode_image(image)
    messages = create_message(SYSTEM_ROLE_CONTENT, PROMPT_TEMPLATE, image_base64)

    try:
        response = openai_client.chat.completions.create(
            model='gpt-4o',
            messages = messages,
            temperature = 0.1,
        )
        response = json.loads(response.json())

    except APIConnectionError:
        return {"result": "API connection error occurred. Please try again later."}, ""

    print(f'[DEBUG] response: {response}')
    output = response["choices"][0]["message"]["content"]

    # 正規表現でdict形式の文字列を抽出
    pattern = r'(\{.*?\})'
    match = re.search(pattern, output, re.DOTALL)
    if match:
        output = match.group(1)  # dict形式の文字列を抽出
        output = json.loads(output)  # json形式に変換
        verification_status = verify_output(output)  # 出力の検証
        return output, verification_status
    else:
        return None, None
