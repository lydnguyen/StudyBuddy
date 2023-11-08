import random
import logging
import logging.config
from _model import *
from _access_source import ListQuestionaire
from telegram import (
    Poll,
    Update,
    ReplyKeyboardMarkup
)
from telegram.ext import (
    ContextTypes,
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


async def quiz(update : Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a predefined poll"""
    reply_keyboard = [['/start_quiz']]
    quiz_question = get_question_object()
    message = await update.effective_message.reply_poll(
        question=quiz_question.question
        , options=quiz_question.answers
        , type=Poll.QUIZ
        , correct_option_id=quiz_question.correct_answer_position
        , is_anonymous=False
        , allows_multiple_answers=True
        , reply_markup=ReplyKeyboardMarkup(
            reply_keyboard
            , one_time_keyboard=False
            , resize_keyboard=True
        )
    )
    # Save some info about the poll the bot_data for later use in receive_quiz_answer
    payload = {
        message.poll.id: {
            "chat_id": update.effective_chat.id
            , "message_id": message.message_id
        }
    }
    context.bot_data.update(payload)


async def receive_quiz_answer(update : Update, context: ContextTypes.DEFAULT_TYPE, total_vote_count) -> None:
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
