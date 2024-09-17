# import requests
# from telegram import Update
# from telegram.ext import Updater, CommandHandler, CallbackContext
#
# url = "https://api.telegram.org/bot6621187432:AAGxMHa_6X3KFH52O9-4cBKpOlIEukT71hc/sendMessage"
#
# payload = 'chat_id=6261265168&text=/start_quiz'
#
# headers = {
#   'Content-Type': 'application/x-www-form-urlencoded'
# }
#
# response = requests.request("POST", url, headers=headers, data=payload)
#
# print(response.text)
#
#
# def auto_send_command(updater):
#   chat_id = "6261265168"
#   updater.bot.send_message(chat_id=chat_id, text="/start_quiz")

#
# import requests
# import json
#
# # url = 'https://api.telegram.org/bot6080017471:AAEzZj8HF_Z9aExJh58w0lg56W1p3jH7jI4/getUpdates'
# url = 'https://api.telegram.org/bot6621187432:AAGxMHa_6X3KFH52O9-4cBKpOlIEukT71hc/getUpdates'
# headers = {
#     'Content-Type': 'application/x-www-form-urlencoded'
# }
#
# response = requests.request("POST", url, headers=headers)
#
# print(json.dumps(response.text, indent=4))


from telethon import TelegramClient

# Replace with your API ID, API hash, and phone number
api_id = '25288375'
api_hash = '8ad2a36c72becd266d4bf9df7ae3eac9'
# phone_number = '+31614991537'
phone_number = '+31614991537'

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)


async def main():
  # Log in if necessary
  await client.start(phone_number)

  # Send message to a chat or channel
  chat_id = 6621187432  # Use @username or channel id
  message = "/start_quiz"

  await client.send_message(chat_id, message)
  #
  # # Fetch all dialogs (chats/channels you're part of)
  # dialogs = await client.get_dialogs()
  #
  # # Print chat/channel names and their IDs
  # for dialog in dialogs:
  #   print(f"Chat/Channel: {dialog.name}, ID: {dialog.id}")


with client:
  client.loop.run_until_complete(main())


#
test = {
    "ok": true,
    "result": [
        {
            "update_id": 262629189,
            "message": {
                "message_id": 1029,
                "from": {
                    "id": 6261265168,
                    "is_bot": false,
                    "first_name": "Lan",
                    "last_name": "Nguyen",
                    "language_code": "en"
                },
                "chat": {
                    "id": 6261265168,
                    "first_name": "Lan",
                    "last_name": "Nguyen",
                    "type": "private"
                },
                "date": 1726226659,
                "text": "/start_quiz",
                "entities": [
                    {
                        "offset": 0,
                        "length": 11,
                        "type": "bot_command"
                    }
                ]
            }
        },
        {
            "update_id": 262629190,
            "message": {
                "message_id": 1030,
                "from": {
                    "id": 6261265168,
                    "is_bot": false,
                    "first_name": "Lan",
                    "last_name": "Nguyen",
                    "language_code": "en"
                },
                "chat": {
                    "id": -992109719,
                    "title": "Study budy group",
                    "type": "group",
                    "all_members_are_administrators": true
                },
                "date": 1726226672,
                "new_chat_participant": {
                    "id": 6621187432,
                    "is_bot": true,
                    "first_name": "StudyBuddy_dev",
                    "username": "StudyBuddy_dev_bot"
                },
                "new_chat_member": {
                    "id": 6621187432,
                    "is_bot": true,
                    "first_name": "StudyBuddy_dev",
                    "username": "StudyBuddy_dev_bot"
                },
                "new_chat_members": [
                    {
                        "id": 6621187432,
                        "is_bot": true,
                        "first_name": "StudyBuddy_dev",
                        "username": "StudyBuddy_dev_bot"
                    }
                ]
            }
        }
    ]
}
#
# from telegram.ext import (
#     Application,
#     CommandHandler,
#     CallbackQueryHandler
# )
#
#
#
# application = Application.builder().token(DefaultConfig.TELEGRAM_TOKEN).build()
#
# application.add_handler(CommandHandler('start', start))
#
#
#
