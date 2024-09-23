import requests

api_root = "https://linguee-api.fly.dev/api/v2"
resp = requests.get(f"{api_root}/translations", params={"query": "Anzeige", "src": "de", "dst": "en"})
print(resp.json())
for lemma in resp.json():
    print(lemma)
    for translation in lemma['translations']:
        print(f"{lemma['text']} -> {translation['text']}")