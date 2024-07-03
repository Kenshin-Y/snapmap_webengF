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
        "description_probability": 0.85,
        "photo_app": "Instagram",
        "photo_app_probability": 0.95,
    }
    ```
    """


def get_gpt_openai_apikey():
    with open("secret.json") as f:
        secret = json.load(f)
    return secret["OPENAI_API_KEY"]


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


def gen_chat_response_with_gpt4(image: Image) -> dict:
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
        return output
    else:
        return None
