
import random
from celery import shared_task
from .models import RandomNumber
from .crowling import kun_uz, daryo_uz, store_tags, write_data


@shared_task(name="crowling_news")
def crowler_task():

    #ranum = random.randint(0,100)
    kun_uz()
    daryo_uz()

    write_data()

    store_tags()


    # RandomNumber.objects.create(numb=ranum)