from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest, DeleteMessagesRequest
from telethon.tl.types import InputPeerChannel

# Укажите ваши данные авторизации

api_id = ''#айди приложения из https://my.telegram.org/apps
api_hash = ''#хэш приложения из https://my.telegram.org/apps
phone = ''#номер телефона телеграм аккаунта


channel_username = 'https://t.me/+CHCFZQ21mUdmMjMy'  # Имя пользователя вашего канала

#Все выше данные вписываются внутрь одинарных ковычек

# Создание клиента
client = TelegramClient('session_name', api_id, api_hash)


def main():
    try:
        client.connect()

        # Ensure you're authorized
        if not client.is_user_authorized():
            client.send_code_request(phone)
            try:
                client.sign_in(phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                client.sign_in(password=input('Password: '))

        # Получение объекта канала
        channel = client.get_entity(channel_username)

        # Получение истории сообщений
        offset_id = 0
        limit = 100
        all_message_ids = []

        while True:
            history = client(GetHistoryRequest(
                peer=channel,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            ))

            if not history.messages:
                break

            messages = history.messages
            message_ids = [msg.id for msg in messages]
            all_message_ids.extend(message_ids)
            offset_id = messages[-1].id
            print(f"Retrieved {len(message_ids)} messages")

        # Удаление сообщений
        for message_id in all_message_ids:
            client.delete_messages(channel, [message_id])
            print(f"Deleted message with id: {message_id}")

        print("All messages deleted")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        client.disconnect()


if __name__ == "__main__":
    main()