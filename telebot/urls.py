from django.conf.urls import url
from . import views
import logging
from telegram.ext import Updater, Job
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from .views import CommandReceiveView

urlpatterns = [
    url(r'^bot/(?P<bot_token>.+)/$', CommandReceiveView.as_view(), name='command'),
    #url(r'^bot/(?P<bot_token>.+)/$', CommandReceiveView.as_view(), name='command'),
]


updater = Updater(token='344944268:AAFBk3-f-SJVq4xxEkn5ktlt2KN5htUsa88')
j = updater.job_queue
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.sendMessage(chat_id=update.message.chat_id, text=text_caps)

def callback_minute(bot, job):
    bot.sendMessage(chat_id='99601112', text='One message every minute')


job_minute = Job(callback_minute, 60.0)
j.put(job_minute, next_t=0.0)


def callback_30(bot, job):
    bot.sendMessage(chat_id='99601112', text='A single message with 30s delay')

j.put(Job(callback_30, 30.0, repeat=False))

job_minute.enabled = False  # Temporarily disable this job
job_minute.schedule_removal()  # Remove this job completely


caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()