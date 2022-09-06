
import random
from celery import shared_task
from .models import RandomNumber


@shared_task(name="crowling_news")
def crowler_task():

    ranum = random.randint(0,100)

    RandomNumber.objects.create(numb=ranum)