import pyfiglet
import logging
import logging.config
import os
from _authentications import Authenticate
import _quiz_generator as qg
from telegram import (
    Update,
)
from telegram.ext import (
    Application,
    CommandHandler,
)


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


def main():
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(DefaultConfig.TELEGRAM_TOKEN).build()
    quiz_handler = CommandHandler('start_quiz', qg.quiz)
    application.add_handler(quiz_handler)

    # receive_q_answer = PollHandler(DefaultConfig.TOTAL_VOTER_COUNT, qg.receive_quiz_answer)
    # application.add_handler(receive_q_answer)

    # log all errors
    application.add_error_handler(error)

    # Run the bot until user press Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("Study Buddy Quiz")
    print(ascii_banner)

    # Enable logging
    DefaultConfig.init_logging()

    main()
