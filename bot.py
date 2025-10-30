import requests

from config import TOKEN

TG_BOT_URL = f'https://api.telegram.org/bot{TOKEN}'


def get_updates(offset: int | None, limit: int = 100):
    url = f'{TG_BOT_URL}/getUpdates'
    params = {
        'offset': offset,
        'limit': limit
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()['result']
    
def send_message(chat_id: int | str, text: str):
    url = f'{TG_BOT_URL}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': text
    }
    requests.get(url, params=params)
    
def send_photo(chat_id: int | str, photo: str):
    url = f'{TG_BOT_URL}/sendPhoto'
    params = {
        'chat_id': chat_id,
        'photo': photo
    }
    requests.get(url, params=params)
    
def send_location(chat_id: int | str, latitude: float, longitude: float):
    url = f'{TG_BOT_URL}/sendLocation'
    params = {
        'chat_id': chat_id,
        'latitude': latitude,
        'longitude': longitude,
    }
    requests.get(url, params=params)

def main():
    offset = None
    limit = 100

    while True:
        for update in get_updates(offset, limit):
            chat_id = update['message']['chat']['id']

            if 'text' in update['message']:
                text = update['message']['text']
                if text == '/start':
                    # add user to database
                    text = 'salom, botga xush kelibsiz!'

                send_message(chat_id, text)
            elif 'photo' in update['message']:
                photo = update['message']['photo'][-1]
                send_photo(chat_id, photo['file_id'])
            elif 'location' in update['message']:
                location = update['message']['location']
                send_location(chat_id, location['latitude'], location['longitude'])

            offset = update['update_id'] + 1

main()
