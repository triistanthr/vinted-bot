import requests
import time

# =========================
# CONFIG
# =========================

TOKEN = "8719596540:AAFbztZMrwNjc4v49yziUUSq4rgYjQujsSg"
CHAT_ID = "5552183707"

# URL Vinted avec tes filtres
URL = (
    "https://www.vinted.fr/api/v2/catalog/items?"
    "search_text=&"
    "catalog[]=5&"
    "brand_ids[]=88&"
    "size_ids[]=207&size_ids[]=208&size_ids[]=209&"
    "material_ids[]=14&"
    "price_to=40&"
    "order=newest_first"
)

seen_ids = set()

# =========================
# TELEGRAM
# =========================

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

# =========================
# VINTED CHECK
# =========================

def check_vinted():
    global seen_ids

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(URL, headers=headers)

    data = r.json()

    items = data.get("items", [])

    for item in items:

        item_id = item["id"]

        if item_id not in seen_ids:

            seen_ids.add(item_id)

            title = item["title"]
            price = item["price"]
            size = item.get("size_title", "?")
            brand = item.get("brand_title", "?")
            url = item["url"]

            message = (
                f"🆕 Nouvelle annonce Vinted\n\n"
                f"👕 {title}\n"
                f"🏷️ {brand}\n"
                f"📏 Taille : {size}\n"
                f"💰 {price} €\n\n"
                f"{url}"
            )

            send_telegram(message)

            print("Nouvelle annonce envoyée")

# =========================
# LOOP
# =========================

print("Bot Vinted lancé...")

while True:
    try:
        check_vinted()
    except Exception as e:
        print("Erreur :", e)

    time.sleep(30)
