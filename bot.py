import json
import requests
from config import TOKEN

bot_url = f"https://api.telegram.org/bot{TOKEN}"
users_file = "users.json"


def load_users():
    try:
        with open(users_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_users(users):
    with open(users_file, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def add_user(user):
    users = load_users()
    mavjud = any(u["id"] == user["id"] for u in users)
    if not mavjud:
        users.append(user)
        save_users(users)


def get_updates(offset=None):
    url = f"{bot_url}/getUpdates"
    params = {"offset": offset, "timeout": 20}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        return r.json()["result"]
    return []


def send_message(chat_id, text):
    url = f"{bot_url}/sendMessage"
    requests.get(url, params={"chat_id": chat_id, "text": text})


def send_photo(chat_id, file_id):
    url = f"{bot_url}/sendPhoto"
    requests.get(url, params={"chat_id": chat_id, "photo": file_id})


def send_video(chat_id, file_id):
    url = f"{bot_url}/sendVideo"
    requests.get(url, params={"chat_id": chat_id, "video": file_id})


def send_audio(chat_id, file_id):
    url = f"{bot_url}/sendAudio"
    requests.get(url, params={"chat_id": chat_id, "audio": file_id})


def send_voice(chat_id, file_id):
    url = f"{bot_url}/sendVoice"
    requests.get(url, params={"chat_id": chat_id, "voice": file_id})


def send_document(chat_id, file_id):
    url = f"{bot_url}/sendDocument"
    requests.get(url, params={"chat_id": chat_id, "document": file_id})


def send_contact(chat_id, phone, name):
    url = f"{bot_url}/sendContact"
    params = {"chat_id": chat_id, "phone_number": phone, "first_name": name}
    requests.get(url, params=params)


def send_dice(chat_id):
    url = f"{bot_url}/sendDice"
    requests.get(url, params={"chat_id": chat_id})


def main():
    offset = None
    print("Bot ishga tushdi...")

    while True:
        updates = get_updates(offset)

        for update in updates:
            msg = update.get("message", {})
            chat_id = msg["chat"]["id"]
            offset = update["update_id"] + 1

            # /start komandasi
            if "text" in msg and msg["text"] == "/start":
                user = {
                    "id": chat_id,
                    "first_name": msg["from"].get("first_name"),
                    "username": msg["from"].get("username")
                }
                add_user(user)
                send_message(chat_id, "Salom! Botga xush kelibsiz 😊")
                continue

            # Echo: send back exactly what was received (text, photo, video, audio, voice, document, contact, dice)
            if "text" in msg:
                send_message(chat_id, msg["text"])
            elif "photo" in msg:
                send_photo(chat_id, msg["photo"][-1]["file_id"])
            elif "video" in msg:
                send_video(chat_id, msg["video"]["file_id"])
            elif "audio" in msg:
                send_audio(chat_id, msg["audio"]["file_id"])
            elif "voice" in msg:
                send_voice(chat_id, msg["voice"]["file_id"])
            elif "document" in msg:
                send_document(chat_id, msg["document"]["file_id"])
            elif "contact" in msg:
                c = msg["contact"]
                send_contact(chat_id, c["phone_number"], c["first_name"])
            elif "dice" in msg:
                send_dice(chat_id)
            else:
                send_message(chat_id, "Bu turdagi faylni yubora olmayman.")


if __name__ == "__main__":
    main()
