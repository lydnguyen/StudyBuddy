import time
import yaml
import random
import pyfiglet
import logging
import logging.config
import sys
import os
from dotenv import load_dotenv, find_dotenv
import telegram
from _model import *
from _authentications import Authenticate
from _access_source import ListQuestionaire
from telegram import (
    KeyboardButton,
    KeyboardButtonPollType,
    Poll,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PollAnswerHandler,
    PollHandler,
    filters,
)


def get_question_object():
    """Send a message when the command /start is issued."""
    question = questionaire_generator()
    question_content = question['question']
    answer = question['options']
    correct_answer_pos = question['correct_answer_position']
    correct_answer = answer[correct_answer_pos]

    quiz_question = QuizQuestion()
    quiz_question.question = question_content
    quiz_question.answers = answer
    quiz_question.correct_answer_position = correct_answer_pos
    quiz_question.correct_answer = correct_answer

    return quiz_question


def questionaire_generator():
    questions = ListQuestionaire().get_all_questions_available()
    question_id = random.choice(list(questions.keys()))
    logging.info(f'Question ID: {question_id}')
    return questions[question_id]


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a predefined poll"""
    quiz_question = get_question_object()
    message = await update.effective_message.reply_poll(
        question=quiz_question.question
        , options=quiz_question.answers
        , type=Poll.QUIZ
        , correct_option_id=quiz_question.correct_answer_position
        , is_anonymous=False
        , allows_multiple_answers=True
    )
    # Save some info about the poll the bot_data for later use in receive_quiz_answer
    payload = {
        message.poll.id: {
            "chat_id": update.effective_chat.id
            , "message_id": message.message_id
        }
    }
    context.bot_data.update(payload)


async def receive_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, total_vote_count) -> None:
    """Close quiz after three participants took it"""
    # the bot can receive closed poll updates we don't care about
    if update.poll.is_closed:
        return
    if update.poll.total_voter_count == total_vote_count:
        try:
            quiz_data = context.bot_data[update.poll.id]
        # this means this poll answer update is from an old poll, we can't stop it then
        except KeyError:
            return
        await context.bot.stop_poll(quiz_data["chat_id"], quiz_data["message_id"])


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
    application = Application.builder().token(DefaultConfig.TELEGRAM_TOKEN).build()
    start_handler = CommandHandler('s', quiz)
    receive_q_answer = PollHandler(DefaultConfig.TOTAL_VOTER_COUNT, receive_quiz_answer)

    application.add_handler(start_handler)
    application.add_handler(receive_q_answer)

    # log all errors
    application.add_error_handler(error)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("Study Buddy Quiz")
    print(ascii_banner)

    # Enable logging
    DefaultConfig.init_logging()

    main()
