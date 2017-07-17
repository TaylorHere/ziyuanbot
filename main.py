#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from uuid import uuid4

import re

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent, InlineQueryResult
from telegram.ext import Updater, InlineQueryHandler, \
    CommandHandler, MessageHandler, Filters, ChosenInlineResultHandler
import logging

from model import Record
from db_config import init_db, db_session
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def command_start(bot, update):
    help(bot, update, 'talk')


def command_help(bot, update):
    help(bot, update, 'talk')


def command_search(bot, update):
    search(bot, update, 'talk')


def command_add(bot, update):
    add(bot, update, 'talk')


def isURL(query):
    if '://' in query:
        return True
    return False


def help(bot, update, mode):
    update.message.reply_text(
        """
hi！你可以使用@ziyuanbot来记录和搜索资源，@ziyuanbot仅仅记录url，并提供简单的搜索功能。
        """
    )


def search(bot, update, mode):
    if mode == 'talk':
        update.message.reply_text('search!')
    elif mode == 'inline':
        results = list()
        query = update.inline_query.query
        results.append(InlineQueryResultArticle(
            id=uuid4(),
            title="找到以下结果",
            input_message_content=InputTextMessageContent("我在使用@ziyuanbot搜索资源%s" % query)))

        if query == ' ':
            records = Record.query.all()
        else:
            print(query)
            filter_str = u"%" + query + u"%"
            print(filter_str)
            records = Record.query.filter(
                Record.keys.like(filter_str)).all()
            print(records)
        for record in records:
            results.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=record.keys or "no keys",
                    input_message_content=InputTextMessageContent("我在@ziyuanbot找到了一条资源%s" % record.url)))
        update.inline_query.answer(results)


def add(bot, update, mode):
    if mode == 'talk':
        update.message.reply_text('add!')
    elif mode == 'inline':
        results = list()
        query = update.inline_query.query
        results.append(InlineQueryResultArticle(id=uuid4(),
                                                title="点击添加记录",
                                                input_message_content=InputTextMessageContent("我向@ziyuanbot添加了一个资源%s" % query)))
        update.inline_query.answer(results)


def inlinequery(bot, update):
    query = update.inline_query.query
    if isURL(query):
        add(bot, update, 'inline')
    else:
        search(bot, update, 'inline')


def chose(bot, update):
    global db_session
    query = update.chosen_inline_result.query
    if isURL(query):
        record = Record().featch(url=query)
        db_session.add(record)
        db_session.commit()
    pass


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(token='400632441:AAE9AlwTOgqeLakW4De2VRjkVNxp0iREU78')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", command_start))
    dp.add_handler(CommandHandler("help", command_help))
    dp.add_handler(CommandHandler("search", command_search))
    dp.add_handler(CommandHandler("add", command_add))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_handler(ChosenInlineResultHandler(chose))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    print('bot is running....')
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    init_db()
    main()
# # # #!/usr/bin/env python
# # # # -*- coding: utf-8 -*-
# # # #
# # # # Simple Bot to reply to Telegram messages. This is built on the API wrapper, see
# # # # echobot2.py to see the same example built on the telegram.ext bot framework.
# # # # This program is dedicated to the public domain under the CC0 license.
# # # import logging
# # # import telegram
# # # from telegram.error import NetworkError, Unauthorized
# # # from time import sleep


# # # update_id = None


# # # def main():
# # #     global update_id
# # #     # Telegram Bot Authorization Token
# # #     bot = telegram.Bot('400632441:AAE9AlwTOgqeLakW4De2VRjkVNxp0iREU78')

# # #     # get the first pending update_id, this is so we can skip over it in case
# # #     # we get an "Unauthorized" exception.
# # #     try:
# # #         update_id = bot.get_updates()[0].update_id
# # #     except IndexError:
# # #         update_id = None

# # #     logging.basicConfig(
# # #         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# # #     while True:
# # #         try:
# # #             echo(bot)
# # #         except NetworkError:
# # #             sleep(1)
# # #         except Unauthorized:
# # #             # The user has removed or blocked the bot.
# # #             update_id += 1


# # # def echo(bot):
# # #     global update_id
# # #     # Request updates after the last update_id
# # #     for update in bot.get_updates(offset=update_id, timeout=10):
# # #         update_id = update.update_id + 1

# # #         if update.message:  # your bot can receive updates without messages
# # #             # Reply to the message
# # #             update.message.reply_text(update.message.text)


# # # if __name__ == '__main__':
# # #     main()
# # #!/usr/bin/env python
# # # -*- coding: utf-8 -*-
# # #
# # # Basic example for a bot that uses inline keyboards.
# # # This program is dedicated to the public domain under the CC0 license.

# # import logging
# # from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# # from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# # logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
# #                     level=logging.INFO)


# # def start(bot, update):
# #     keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
# #                  InlineKeyboardButton("Option 2", callback_data='2')],

# #                 [InlineKeyboardButton("Option 3", callback_data='3')]]

# #     reply_markup = InlineKeyboardMarkup(keyboard)

# #     update.message.reply_text('Please choose:', reply_markup=reply_markup)


# # def button(bot, update):
# #     query = update.callback_query

# #     bot.edit_message_text(text="Selected option: %s" % query.data,
# #                           chat_id=query.message.chat_id,
# #                           message_id=query.message.message_id)


# # def help(bot, update):
# #     update.message.reply_text("Use /start to test this bot.")


# # def error(bot, update, error):
# #     logging.warning('Update "%s" caused error "%s"' % (update, error))


# # # Create the Updater and pass it your bot's token.
# # updater = Updater("400632441:AAE9AlwTOgqeLakW4De2VRjkVNxp0iREU78")

# # updater.dispatcher.add_handler(CommandHandler('start', start))
# # updater.dispatcher.add_handler(CallbackQueryHandler(button))
# # updater.dispatcher.add_handler(CommandHandler('help', help))
# # updater.dispatcher.add_error_handler(error)

# # # Start the Bot
# # updater.start_polling()

# # # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# # # SIGTERM or SIGABRT
# # updater.idle()
# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# #
# # Simple Bot to reply to Telegram messages
# # This program is dedicated to the public domain under the CC0 license.
# """
# This Bot uses the Updater class to handle the bot.
# First, a few handler functions are defined. Then, those functions are passed to
# the Dispatcher and registered at their respective places.
# Then, the bot is started and runs until we press Ctrl-C on the command line.
# Usage:
# Basic Echobot example, repeats messages.
# Press Ctrl-C on the command line or send a signal to the process to stop the
# bot.
# """

# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
# import logging

# # Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)

# logger = logging.getLogger(__name__)


# # Define a few command handlers. These usually take the two arguments bot and
# # update. Error handlers also receive the raised TelegramError object in error.
# def start(bot, update):
#     update.message.reply_text('Hi!')


# def help(bot, update):
#     update.message.reply_text('Help!')


# def echo(bot, update):
#     update.message.reply_text(update.message.text)


# def error(bot, update, error):
#     logger.warn('Update "%s" caused error "%s"' % (update, error))


# def main():
#     # Create the EventHandler and pass it your bot's token.
#     updater = Updater("400632441:AAE9AlwTOgqeLakW4De2VRjkVNxp0iREU78")

#     # Get the dispatcher to register handlers
#     dp = updater.dispatcher

#     # on different commands - answer in Telegram
#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(CommandHandler("help", help))

#     # on noncommand i.e message - echo the message on Telegram
#     dp.add_handler(MessageHandler(Filters.text, echo))

#     # log all errors
#     dp.add_error_handler(error)

#     # Start the Bot
#     updater.start_polling()

#     # Run the bot until you press Ctrl-C or the process receives SIGINT,
#     # SIGTERM or SIGABRT. This should be used most of the time, since
#     # start_polling() is non-blocking and will stop the bot gracefully.
#     updater.idle()


# if __name__ == '__main__':
#     main()
