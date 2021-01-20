from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
import logging, requests, re, datetime

# Youtube API Key
yt_key = "AIzaSyC6_rMCD5YaEtTx9ThFhBq5mIPtvTAS2dE"

# Youtube channel about stocks
channels = { "sta": { "id": "UCCDgQxJyWEfn5R68JsMpS4A", "nick": "Om Silent 🤫🤫🤫" },
            "em": { "id": "UCsoCGo9AfIC6T95pdusa14g", "nick": "Miss Ellen 🥵🥵🥵" },
            "astronacci": { "id": "UCYRFEuGLfXFFvbq2-nStY9w", "nick": "Om Gema 😎😎😎 "},
            "cnbc": { "id": "UCGN9JsnkvK05v2lnTI_-uGA", "nick": "CNBC Indonesia 💼💼💼" },
            "wiguna": { "id": "UCNXGbmpTzugVyH4xigHCnAQ", "nick": "Om Wiguna 🤑🤑🤑" },
            "idx": { "id": "UCn8U8GiaHZNP9pFKzl3Cwlg", "nick": "IDX Channel ☕️☕️☕️" }  
            }

updater = Updater(token='1549117924:AAFtjT7yAwBVdiwEz-M10y3Lm9Ky9cACxQ0', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, selamat datang di bot maififteen v1.0.0\nBot untuk mendapatkan video terbaru tentang saham dari maestro saham Indonesia\n\nList commands\n/sta - dari om silent\n/em - dari miss ellen\n/astro - dari om gema\n/cnbc - dari cnbc indonesia\n/wiguna - dari om wiguna\n/idx - dari idx channel\n\nSalam profit rekan-rekan 🚀🚀🚀")

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

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('sta', sta))
dispatcher.add_handler(CommandHandler('em', em))
dispatcher.add_handler(CommandHandler('astro', astronacci))
dispatcher.add_handler(CommandHandler('cnbc', cnbc))
dispatcher.add_handler(CommandHandler('wiguna', wiguna))
dispatcher.add_handler(CommandHandler('idx', idx))

updater.start_polling()

