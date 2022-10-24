
import random
from celery import shared_task
from .models import RandomNumber
from .crowling import Crowler
import time

@shared_task(name="crowling_news")
def crowler_task():
    time.sleep(1)

    
    crowler = Crowler()
    crowler.run()


    ranum = random.randint(0,100)
    RandomNumber.objects.create(numb=ranum)