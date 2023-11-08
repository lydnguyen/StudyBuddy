from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# Source: https://stackoverflow.com/questions/51125356/proper-way-to-build-menus-with-python-telegram-bot


############################### Bot ############################################
async def switch_topic(update, context):
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
