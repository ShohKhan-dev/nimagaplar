from django.contrib import admin

# Register your models here.
from .models import Keywords, News, WatchList, RandomNumber, User, IgnoreList, WaitList


admin.site.register(User)
admin.site.register(News)
admin.site.register(WatchList)
admin.site.register(Keywords)
admin.site.register(RandomNumber)
admin.site.register(IgnoreList)
admin.site.register(WaitList)