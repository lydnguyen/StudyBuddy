from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
import logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
)
# Original source: https://stackoverflow.com/questions/51125356/proper-way-to-build-menus-with-python-telegram-bot

option_info = {
    'AWS CAA03': {'id': 'aws'},
    'English': {'id': 'english'},
    'Math': {'id': 'math'}
}

level_info = {'message': 'Choose level of difficulty:',
              'levels': {
                  'beginner': 'Beginner',
                  'intermediate': 'Intermediate',
                  'advanced': 'Advanced',
                  'main': 'Main Menu',
              }}

topic = ''
level = ''


############################### Menus ############################################
async def switch_topic(update, context):
    await update.message.reply_text(text='Choose the option in main menu:',
                                    reply_markup=await main_menu_keyboard())


async def main_menu(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text='Choose the option in main menu:',
        reply_markup=await main_menu_keyboard())


async def level_menu(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=level_info['message'],
        reply_markup=await level_menu_keyboard())
    global topic
    if query.data:
        topic = query.data
    logging.info(f'User choose for topic: {topic}')


async def return_options(update, context):
    query = update.callback_query
    await query.answer()

    global level
    if query.data:
        level = query.data
    logging.info(f'User choose for level: {level}')

    await query.edit_message_text(
        text=f'You are now quizing for topic {topic.upper()}, level {level.upper()}.',
    )


############################ Keyboards #########################################
async def main_menu_keyboard():
    keyboard = []
    for option, callback_data in option_info.items():
        button = [InlineKeyboardButton(text=option, callback_data=callback_data['id'])]
        keyboard.append(button)
    return InlineKeyboardMarkup(keyboard)


async def level_menu_keyboard():
    keyboard = []
    for value, key in level_info['levels'].items():
        button = [InlineKeyboardButton(text=key, callback_data=value)]
        keyboard.append(button)
    return InlineKeyboardMarkup(keyboard)

