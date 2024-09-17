import pyfiglet
import logging
import logging.config
import os
import datetime
from _quiz_generator import send_quiz_poll_scheduler
from _authentications import Authenticate
from _access_source import ListQuestionaire
import _quiz_generator as qg
import _menu_options as mo
from telegram import (
    Update,
    ReplyKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler
)
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


def error(update, context):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" ', update)
    logging.exception(context.error)


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


async def start(update, context):
    reply_keyboard = [["/start_quiz", "/switch_topic"]]
    keyboard = ReplyKeyboardMarkup(reply_keyboard
                                   , one_time_keyboard=False
                                   , resize_keyboard=True
                                   )
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Welcome to your own Study Buddy. \n Which topic do you want?",
                                   reply_markup=keyboard,
                                   )


def main():
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(DefaultConfig.TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler(['next_question', 'start_quiz'], qg.quiz))
    application.add_handler(CommandHandler(['choose_topic', 'switch_topic'], mo.switch_topic))

    option_info, level_info = ListQuestionaire().fetch_question_options()
    for i in option_info.values():
        application.add_handler(CallbackQueryHandler(mo.level_menu, pattern=i['id']))
    for topic, levels in level_info['levels'].items():
        for level in levels:
            if 'main' in level:
                application.add_handler(CallbackQueryHandler(mo.main_menu, pattern=level))
            else:
                application.add_handler(CallbackQueryHandler(mo.return_options, pattern=level))

    # application.add_handler(PollHandler(DefaultConfig.TOTAL_VOTER_COUNT, qg.receive_quiz_answer)

    # log all errors
    application.add_error_handler(error)

    times = [
        datetime.datetime.now() + datetime.timedelta(seconds=5)
        , datetime.datetime.now() + datetime.timedelta(seconds=7)
        , datetime.datetime.now() + datetime.timedelta(seconds=10)
    ]
    for time in times:
        application.job_queue.run_daily(
            callback=send_quiz_poll_scheduler
            , time=time.astimezone()
            , job_kwargs={'misfire_grace_time': 10}  # Adding grace time for misfire
        )

    # Run the bot until user press Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("Study Buddy Quiz")
    print(ascii_banner)

    # Enable logging
    DefaultConfig.init_logging()

    main()
