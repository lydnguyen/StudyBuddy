from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ForceReply, Update
from telegram.ext import Updater
import configparser
from telegram.ext import *
import os
from _authentications import Authenticate
import logging
import pyfiglet

# config = configparser.ConfigParser()
# config.read("config/config.ini")
#
# admins = config["Users"]["admins"]


############################### Bot ############################################
async def start(update, context):
    await update.message.reply_text(await main_menu_message(),
                                    reply_markup=await main_menu_keyboard())


async def main_menu(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=await main_menu_message(),
        reply_markup=await main_menu_keyboard())


async def first_menu(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=await first_menu_message(),
        reply_markup=await first_menu_keyboard())


async def second_menu(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=await second_menu_message(),
        reply_markup=await second_menu_keyboard())


async def third_menu(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=await third_menu_message(),
        reply_markup=await third_menu_keyboard())


# and so on for every callback_data option
async def first_submenu(bot, update):
    pass


async def second_submenu(bot, update):
    pass


############################ Keyboards #########################################
async def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Option 1', callback_data='m1')],
                [InlineKeyboardButton('Option 2', callback_data='m2')],
                [InlineKeyboardButton('Option 3', callback_data='m3')]]
    return InlineKeyboardMarkup(keyboard)


async def first_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
                [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


async def second_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
                [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


async def third_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Submenu 3-1', callback_data='m2_1')],
                [InlineKeyboardButton('Submenu 3-2', callback_data='m2_2')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


############################# Messages #########################################
async def main_menu_message():
    return 'Choose the option in main menu:'


async def first_menu_message():
    return 'Choose the submenu in first menu:'


async def second_menu_message():
    return 'Choose the submenu in second menu:'


async def third_menu_message():
    return 'Choose the submenu in second menu:'


class DefaultConfig:
    TELEGRAM_TOKEN = Authenticate().get_secret()['telegram_token_dev']
    PORT = int(os.environ.get("PORT", 3978))
    MODE = os.environ.get("MODE", "polling")
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")
    TOTAL_VOTER_COUNT = 1

    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

    @staticmethod
    def init_logging():
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=DefaultConfig.LOG_LEVEL,
        )

############################# Handlers #########################################
# Create the Application and pass it your bot's token.
def main() -> None:
    bot_token = DefaultConfig.TELEGRAM_TOKEN
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    application.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
    application.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
    application.add_handler(CallbackQueryHandler(third_menu, pattern='m3'))

    application.add_handler(CallbackQueryHandler(first_submenu,
                                                 pattern='m1_1'))
    application.add_handler(CallbackQueryHandler(second_submenu,
                                                 pattern='m2_1'))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("Study Buddy Quiz")
    print(ascii_banner)

    # Enable logging
    DefaultConfig.init_logging()
    main()
