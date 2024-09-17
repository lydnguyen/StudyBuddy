import random
import logging
import logging.config
# from telegram_bot._model import *
# from telegram_bot._access_source import ListQuestionaire
from _model import *
from _access_source import ListQuestionaire
from telegram import (
    Poll,
    Update,
)
from telegram.ext import (
    ContextTypes,
)


def get_question_object(quizid: int):
    """Send a message when the command /start is issued."""
    question = questionaire_generator(quizid)
    question_content = question['question']
    # Generate each time a shuffled list of options so that the option does not
    # remain on the same order
    options = question['options']
    options_list = list(options.values())
    random.shuffle(options_list)
    correct_answer_position = ''
    for i in options_list:
        if i == options[question['correct_optionid']]:
            correct_answer_position = options_list.index(i)
    correct_option = options_list[correct_answer_position]

    quiz_question = QuizQuestion()
    quiz_question.question = question_content
    quiz_question.options = options_list
    quiz_question.correct_answer_position = correct_answer_position
    quiz_question.correct_answer = correct_option
    logging.info(f'Get all quiz objects for quesion: {question_content}')
    return quiz_question


def questionaire_generator(quizid: int):
    questions = ListQuestionaire().fetch_data(quizid)
    question_id = random.choice(list(questions.keys()))
    logging.info(f'Generate quiz for QuestionID: {question_id}')
    return questions[question_id]


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a predefined poll"""
    userid = update.message.from_user.id
    quizid = ListQuestionaire().fetch_chosen_quiztopic(participantid=userid)

    logging.info(f'user id {userid} has quizid {quizid}')
    quiz_question = get_question_object(quizid)

    logging.info('Update quiz form in telegram')
    message = await update.effective_message.reply_poll(
        question=quiz_question.question
        , options=quiz_question.options
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
    logging.info('done quiz')


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


async def send_quiz_poll_scheduler(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a predefined poll"""
    userid = 6261265168
    quizid = ListQuestionaire().fetch_chosen_quiztopic(participantid=userid)

    logging.info(f'----------------------------------------')

    # logging.info(f'user id {userid} has quizid {quizid}')
    quiz_question = get_question_object(quizid)

    # logging.info('Update quiz form in telegram')
    await context.bot.send_poll(
        chat_id=userid
        , question=quiz_question.question
        , options=quiz_question.options
        , type=Poll.QUIZ
        , correct_option_id=quiz_question.correct_answer_position
        , is_anonymous=False
        , allows_multiple_answers=True
    )
    logging.info('Quiz poll sent successfully.')
    logging.info(f'----------------------------------------')