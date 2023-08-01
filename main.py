#!/usr/bin/env python
"""This program is a telegram bot that translates text to desired language.
Before running this program, please create a secrets/configs.py file with
your token as shown below:

TOKEN = "Your-Telegram-Bot-Token-Goes-Here"


author: Dharun
"""

import logging
import sys

from googletrans import Translator
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          InlineQueryHandler, MessageHandler, filters)

import language_list

sys.path.insert(0, 'secrets')
try:
    import configs
except ImportError:
    logging.error("Please create a secrets/configs.py file with your token.",
                  exc_info=True)
    sys.exit(1)

logging.basicConfig(
    format='[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s',
    level=logging.INFO
)


def translate(text, dest_language='en'):
    """This function translates text to a given language

    Args:
        text (string): Text to be translated
        dest_language (str, optional): Destination language the text needs to
        be translated too. Defaults to 'en'.

    Returns:
        string : Translated text
    """
    translator = Translator()
    parts = text.split(" | ")
    if len(parts) == 2:
        dest_language = parts[0]
        text = parts[1]
    else:
        text = parts[0]
    return translator.translate(text, dest=dest_language)


async def start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="I\'m a bot, I can translate text \
to desired language. Type command /help to know more.")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "To translate just enter the text. To translate to specific \
language enter the text in following format\n\n \
Lang Code | Text\n\n \
for example \n\nhi | Hi im a language translator bot\n \
This will translate the text to Hindi. \
Same format follows for inline translation\n \
Type /list to know supported languages. Happy translating!"

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text)


async def list_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Supported languages:\n" + \
        "Language code : Language name\n\n" + \
        '\n'.join([f"`{language_code}` : `{language_name}`" for language_code,
                  language_name in language_list.LANGUAGES.items()])

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                                   parse_mode='Markdown')


async def incoming_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    translated_text = translate(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=translated_text)


async def inline_translator(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=translate(query),
            title='Translate',
            input_message_content=InputTextMessageContent(translate(query))
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Sorry, I didn't understand \
                                   that command")

if __name__ == '__main__':
    application = ApplicationBuilder().token(configs.TOKEN).build()

    start_handler = CommandHandler('start', start)
    supported_languages_handler = CommandHandler('list', list_language)
    help_handler = CommandHandler('help', help)
    incoming_text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND),
                                           incoming_text)
    inline_translator_handler = InlineQueryHandler(inline_translator)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(supported_languages_handler)
    application.add_handler(help_handler)
    application.add_handler(incoming_text_handler)
    application.add_handler(inline_translator_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
