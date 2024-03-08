from pytz import timezone
import pytz
from celery import shared_task
from django.utils import timezone
from datetime import datetime, timedelta

from config import settings
from habits.models import Habit
from habits.services import TelegramBot

tg_bot = TelegramBot()


@shared_task
def send_telegram_notification():
    time_zone = settings.TIME_ZONE
    current_time = datetime.now(pytz.timezone(time_zone))
    # habits_list = Habit.objects.all()
    usefull_habits_list = Habit.objects.filter(is_pleasurable=False)

    for habit in usefull_habits_list:
        local_date = habit.date.astimezone(timezone.get_current_timezone())
        message_main = (f''
                        f'{habit.user.first_name} вам необходимо выполнить привычку - {habit.action} в {local_date}'
                        f'Её нужно выполнить за {habit.time_required} в {habit.place}.'
                        f'После вы получите вознаграждение - {habit.reward} либо {habit.related_habit}.')

        if habit.frequency == 'day' and habit.date <= current_time:
            habit.date = datetime.now(pytz.timezone(time_zone)) + timedelta(days=1)
            message_extended = f'\nДалее ваша привычка должна быть выполнена завтра в {habit.date}.'
            message = message_main + message_extended
            tg_bot.send_message(chat_id=habit.user.telegram, text=message)
            habit.save()

        elif habit.frequency == 'week' and habit.date <= current_time:
            habit.date = datetime.now(pytz.timezone(time_zone)) + timedelta(days=7)
            message_extended = f'\nДалее ваша привычка должна быть выполнена через неделю в {habit.date}.'
            message = message_main + message_extended
            tg_bot.send_message(chat_id=habit.user.telegram, text=message)
            habit.save()
