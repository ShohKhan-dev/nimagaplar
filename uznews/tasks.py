
# import random
# from celery import shared_task
# from .models import RandomNumber
# from .crowling import Crowler
# import time

# @shared_task(name="crowling_news")
# def crowler_task():
#     time.sleep(1)

    
#     crowler = Crowler()
#     crowler.run()


    # ranum = random.randint(0,100)
    # RandomNumber.objects.create(numb=ranum)







from celery import shared_task
from celery.utils.log import get_task_logger

import time

from .crowling import Crowler

logger = get_task_logger(__name__)


@shared_task
def sample_task():
    time.sleep(1)
    print("RUNNING RUNNING!!!!!!")
    
    crowler = Crowler()
    crowler.run()