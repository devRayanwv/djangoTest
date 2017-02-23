import json
import logging
import telepot
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

# Create your views here.

TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)
TelegramBot.setWebhook('https://almodrs.com/bot/344944268:AAFBk3-f-SJVq4xxEkn5ktlt2KN5htUsa88')
logger = logging.getLogger('telegram.bot')


def _display_help():
    return render_to_string('help.md')


class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden("Invalid error")

        commands = {
            '/start': _display_help,
            'help': _display_help,
        }

        raw = request.body.decode('utf-8')
        logging.info(raw)

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest("Invalid request body")

        else:
            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text')

            func = commands.get(cmd.split()[0].lower())

            if func:
                TelegramBot.sendMessage(chat_id, func(), parse_mode='Markdown')
            else:
                TelegramBot.sendMessage(chat_id, 'I do not understand...!')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)

