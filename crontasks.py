
import random

from crowling import kun_uz, daryo_uz, write_data, print_stats

import os
import django


os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()

from uznews.models import RandomNumber
from django.contrib.auth.models import User

import requests

from uznews.models import Keywords, News, RandomNumber

from datetime import datetime

## https://api.telegram.org/bot5390984413:AAE9YbOr7eNpzCCa01nvGZ6T2AR9hSEd2yA/sendMessage?chat_id=5573511547&text=Hi+Everyone

token = '5390984413:AAE9YbOr7eNpzCCa01nvGZ6T2AR9hSEd2yA'

def send_message(usr_id, message):

    response = requests.post(
        url='https://api.telegram.org/bot{0}/{1}'.format(token, "sendMessage"),
        data={'chat_id': usr_id, 'text': message}
    ).json()




def check_all(new_added_news):

    news_queryset = News.objects.filter(id__in={instance.id for instance in new_added_news})
    
    all_users = User.objects.filter(username="5573511547").first()
    result = []
    usr_keywords = all_users.keywords.all()


    for keyword in usr_keywords:
        usr_news = news_queryset.filter(title__icontains=keyword.word)
        for news in usr_news:
            send_message(usr_id=all_users.username, message='https://{}/{}'.format(news.source, news.link))
        

    # for user in all_users:
    #     usr_keywords = user.keywords.all()
    #     for keyword in usr_keywords:
    #         usr_news = News.objects.filter(title__icontains=keyword.word)
    #         for news in usr_news:
    #             send_message(usr_id=user.username, message='https://{}/{}'.format(news.source, news.link))
            

def my_scheduled_job():

    ranum = random.randint(0,100)

    RandomNumber.objects.create(numb=ranum)

    # kun_uz()
    # daryo_uz()
    # write_data()

    # print_stats()

    # check_all(new_added_news)


    

    # number = random.randint(0,100)
    # RandomNumber.objects.create(numb = number)

    # print(number)

    # send_message(usr_id='846062018', message=str(number))



