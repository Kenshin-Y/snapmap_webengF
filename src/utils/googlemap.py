import requests
import json


def get_googlemap_apikey():
    with open("secret.json") as f:
        secret = json.load(f)
    return secret["GOOGLEMAP_API_KEY"]


def get_location_info(output: dict) -> str:
    api_key = get_googlemap_apikey()
    base_url = "https://places.googleapis.com/v1/places:searchText"
    params = {
        "textQuery": output['name'],
        "Content-Type": "application/json",
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress",
        "X-Goog-Api-Key": api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
