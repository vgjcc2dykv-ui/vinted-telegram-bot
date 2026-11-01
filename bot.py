import os
import time
import urllib.parse
import urllib.request
import json

TOKEN = os.environ["BOT_TOKEN"]

RECHERCHES = [
    "Nike Running Division",
    "Nike Running",
    "Pull Nike Tech",
    "Under Armour Hybrid",
    "Veste Under Armour Hybrid",
    "Bas Under Armour Hybrid"
]

def envoyer(chat_id, message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message
    }).encode()
    urllib.request.urlopen(url, data=data)

def traiter(chat_id):
    texte = "🔎 TES RECHERCHES VINTED\n\n"
    for recherche in RECHERCHES:
        lien = "https://www.vinted.fr/catalog?" + urllib.parse.urlencode({
            "search_text": recherche,
            "price_from": 3,
            "price_to": 20
        })
        texte += f"• {recherche}\n{lien}\n\n"
    texte += "Tailles recherchées : S, M, L"
    envoyer(chat_id, texte)

offset = 0

while True:
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset}&timeout=30"
        with urllib.request.urlopen(url) as response:
            updates = json.loads(response.read())

        for update in updates["result"]:
            offset = update["update_id"] + 1
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            if chat_id and message.get("text", "").startswith("/start"):
                traiter(chat_id)

    except Exception:
        time.sleep(5)
