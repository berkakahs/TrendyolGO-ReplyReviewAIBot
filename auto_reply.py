cat > auto_reply.py << 'EOF'
import requests
import base64
import json
import time
import threading
from prettytable import PrettyTable
from flask import Flask, request

# Flask bot webhook
app = Flask(__name__)

# Telegram bot ayarları
BOT_TOKEN = "#burayı doldur#"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
CHAT_ID = "#burayı doldur#"

# API anahtarları
API_KEY = "#burayı doldur#"
API_SECRET = "#burayı doldur#"

# Gemini API bilgileri
GEMINI_API_KEY = "#burayı doldur#"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Kimlik doğrulama işlemi
auth_str = f"{API_KEY}:{API_SECRET}"
auth_base64 = base64.b64encode(auth_str.encode()).decode()

# Header bilgileri
headers = {
    "Authorization": f"Basic {auth_base64}",
    "Content-Type": "application/json",
    "User-Agent": "RESTORANİDYAZ - SelfIntegration"
}

# Trendyol API URL
url = "#burayı doldur#"  # Trendyol API URL'si burada olacak

# Dosya yolları
IGNORED_REVIEWS_FILE = 'ignored_reviews.txt'
PENDING_REVIEWS_FILE = 'pending_reviews.json'

# Bellekte pending yorumlar
pending_reviews = {}

def send_telegram_message(message, reply_markup=None):
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    response = requests.post(f"{TELEGRAM_API_URL}/sendMessage", data=payload)
    if response.status_code != 200:
        print(f"Telegram mesajı gönderilemedi: {response.status_code}")
    else:
        print("Telegram mesajı başarıyla gönderildi.")

def generate_gemini_response(comment_text):
    prompt = f"""
Sana yazıcağım restoran yorumuna uygun ve çok kısa bir cevap ver, Merhaba ile başla, kesinlikle 200 kelimeyi aşmasın, tek satırda olsun. uygun olan bu emojilerden iki tanesini abartmadan kullan:🥗✨💫🙏🏻😣

Yorum: "{comment_text}"
Cevap:
"""
    payload = {"contents": [{"parts": [{"text": prompt.strip()}]}]}
    response = requests.post(GEMINI_URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    else:
        print("Gemini API hata:", response.status_code)
        return "Cevap oluşturulamadı."

def load_ignored_reviews():
    try:
        with open(IGNORED_REVIEWS_FILE, 'r') as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        return set()

def save_ignored_review(review_id):
    with open(IGNORED_REVIEWS_FILE, 'a') as f:
        f.write(f"{review_id}\n")

def load_pending_reviews():
    try:
        with open(PENDING_REVIEWS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_pending_reviews():
    with open(PENDING_REVIEWS_FILE, 'w') as f:
        json.dump(pending_reviews, f)

def fetch_and_process():
    print("Yorumlar kontrol ediliyor...")
    ignored_reviews = load_ignored_reviews()
    existing_pending = load_pending_reviews()

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Yorumlar alınamadı:", response.status_code)
        return

    try:
        data = response.json()
        reviews = data.get("content", [])

        for review in reviews:
            review_id = str(review.get("reviewId"))
            comment_text = review.get("comment", {}).get("text")

            if not review_id or not comment_text:
                continue  # Yorumun ID'si veya metni yoksa geç

            if review_id in ignored_reviews or review_id in existing_pending:
                continue  # Görmezden gelinen veya bekleyen yorumları atla

            response_text = generate_gemini_response(comment_text)
            pending_reviews[review_id] = {
                "comment": comment_text,
                "response": response_text
            }
            save_pending_reviews()

            reply_markup = {
                "inline_keyboard": [
                    [{"text": "👍🏻 Cevabı Gönder", "callback_data": f"approve_{review_id}"}],
                    [{"text": "👎🏻 Görmezden Gel", "callback_data": f"ignore_{review_id}"}]
                ]
            }

            send_telegram_message(
                f"Yorum içeriği:\n{comment_text}\n\nOluşturulan Cevap:\n{response_text}\n\nCevap gönderilsin mi?",
                reply_markup
            )

    except json.JSONDecodeError:
        print("JSON decode hatası:", response.text)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def receive_update():
    update = request.get_json()
    callback_query = update.get("callback_query")
    if not callback_query:
        return "ok"

    data = callback_query.get("data")
    review_id = data.split("_")[1]

    if data.startswith("approve_") and review_id in pending_reviews:
        review_data = pending_reviews.pop(review_id)
        save_pending_reviews()
        reply_url = f"https://api.tgoapis.com/integrator/review/meal/suppliers/976700/stores/288838/reviews/{review_id}/answer"
        reply_response = requests.post(reply_url, headers=headers, json={"text": review_data["response"]})

        if reply_response.status_code == 200:
            send_telegram_message(f"Yorum {review_id} başarıyla yanıtlandı.")
        else:
            send_telegram_message(f"Yorum {review_id} yanıtlanamadı. Hata: {reply_response.status_code}")

    elif data.startswith("ignore_"):
        save_ignored_review(review_id)
        if review_id in pending_reviews:
            pending_reviews.pop(review_id)
            save_pending_reviews()
        send_telegram_message(f"Yorum {review_id} bir daha gösterilmeyecek şekilde görmezden gelindi.")

    return "ok"

def start_flask():
    app.run(port=8443)

if __name__ == "__main__":
    threading.Thread(target=start_flask, daemon=True).start()

    fetch_and_process()  # İlk çalıştırmada hemen yorumları çek

    while True:
        print("20 dakika bekleniyor...")
        time.sleep(1200)
        fetch_and_process()
EOF readme kısmı basıl olsun
