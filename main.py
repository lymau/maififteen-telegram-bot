from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import logging, requests, re, datetime
import os
PORT = int(os.environ.get('PORT', 5000))

# Key
yt_key = "AIzaSyC6_rMCD5YaEtTx9ThFhBq5mIPtvTAS2dE"
TOKEN = '1549117924:AAFtjT7yAwBVdiwEz-M10y3Lm9Ky9cACxQ0'

# Youtube channel about stocks
channels = { "sta": { "id": "UCCDgQxJyWEfn5R68JsMpS4A", "nick": "Om Silent 🤫🤫🤫" },
            "em": { "id": "UCsoCGo9AfIC6T95pdusa14g", "nick": "Miss Ellen 🥵🥵🥵" },
            "astronacci": { "id": "UCYRFEuGLfXFFvbq2-nStY9w", "nick": "Om Gema 😎😎😎 "},
            "cnbc": { "id": "UCGN9JsnkvK05v2lnTI_-uGA", "nick": "CNBC Indonesia 💼💼💼" },
            "wiguna": { "id": "UCNXGbmpTzugVyH4xigHCnAQ", "nick": "Om Wiguna 🤑🤑🤑" },
            "idx": { "id": "UCn8U8GiaHZNP9pFKzl3Cwlg", "nick": "IDX Channel ☕️☕️☕️" }  
            }

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Get Information about bot
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, selamat datang di bot maififteen v1.0.0\nBot untuk mendapatkan video terbaru tentang saham dari maestro saham Indonesia\n\nList commands\n/sta - dari om silent\n/em - dari miss ellen\n/astro - dari om gema\n/cnbc - dari cnbc indonesia\n/wiguna - dari om wiguna\n/idx - dari idx channel\n\nSalam profit rekan-rekan 🚀🚀🚀")

# Get Error
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Function to generate caption by channel Id
def generate_caption(channelId, nick):
    contents = get_latest_video(channelId, yt_key)
    caption = "Ingfo terbaru dari {3}\n\n<a href='https://www.youtube.com/watch?v={0}&channelId={1}'>{2}</a>".format(contents[2],channelId, contents[0], nick)
    return caption

# Function to get data from latest video
# channelId: youtube channel id, key: youtube api key
def get_latest_video(channelId, key):
    contents = requests.get("https://youtube.googleapis.com/youtube/v3/search?maxResults=1&channelId={0}&order=date&part=snippet&key={1}".format(channelId, key)).json()
    snippet_contents = contents["items"][0]["snippet"]
    # Data that to be returned
    title = snippet_contents["title"]
    channel_name = snippet_contents["channelTitle"]
    video_id = contents["items"][0]["id"]["videoId"]
    result = [title, channel_name, video_id]
    return result

# Echo the user sends
def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

# Function for user command
def sta(update, context):
    caption = generate_caption(channels["sta"]["id"], channels["sta"]["nick"])
    context.bot.send_message(parse_mode=ParseMode.HTML, chat_id=update.effective_chat.id, text=caption)

def em(update, context):
    caption = generate_caption(channels["em"]["id"], channels["em"]["nick"])
    context.bot.send_message(parse_mode=ParseMode.HTML, chat_id=update.effective_chat.id, text=caption)

def astronacci(update, context):
    caption = generate_caption(channels["astronacci"]["id"], channels["astronacci"]["nick"])
    context.bot.send_message(parse_mode=ParseMode.HTML, chat_id=update.effective_chat.id, text=caption)

def cnbc(update, context):
    caption = generate_caption(channels["cnbc"]["id"], channels["cnbc"]["nick"])
    context.bot.send_message(parse_mode=ParseMode.HTML, chat_id=update.effective_chat.id, text=caption)

def wiguna(update, context):
    caption = generate_caption(channels["wiguna"]["id"], channels["wiguna"]["nick"])
    context.bot.send_message(parse_mode=ParseMode.HTML, chat_id=update.effective_chat.id, text=caption)

def idx(update, context):
    caption = generate_caption(channels["idx"]["id"], channels["idx"]["nick"])
    context.bot.send_message(parse_mode=ParseMode.HTML, chat_id=update.effective_chat.id, text=caption)

# Send ngaca
def ngaca(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('img/ngaca.png', 'rb'))

# Send cursed bbkp
def bbkp(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('img/bbkpnyahyung.png', 'rb'))
    context.bot.send_video(chat_id=update.effective_chat.id, video=open('img/bbkp_video.mp4', 'rb'), supports_streaming=True)

def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('sta', sta))
    dp.add_handler(CommandHandler('em', em))
    dp.add_handler(CommandHandler('astro', astronacci))
    dp.add_handler(CommandHandler('cnbc', cnbc))
    dp.add_handler(CommandHandler('wiguna', wiguna))
    dp.add_handler(CommandHandler('idx', idx))

    # bonus commands
    dp.add_handler(CommandHandler('ngaca', ngaca))
    dp.add_handler(CommandHandler('bbkp', bbkp))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://damp-savannah-05748.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()
    updater.idle()

if __name__ == '__main__':
    main()