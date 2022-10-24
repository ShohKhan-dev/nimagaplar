from django.conf import settings
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from uznews.models import *

from django.views.generic import ListView, View
from django.http import JsonResponse
from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger

from datetime import datetime, timedelta
import pytz
from django.contrib.admin.views.decorators import staff_member_required
# from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
import re

from django.contrib.auth import authenticate, login

from django.contrib import messages




from .documents import NewsDocument

from elasticsearch_dsl.query import Q



class Helper():

    def clean_keywords(self, text):
        text = text.replace(",", " ").lower()
        text = re.sub("[^a-zA-Z' ]+", "", text)
        keywords = [word.strip().replace("'", "‘") for word in text.split()]
        return keywords


    def get_quaries(self, keywords, interval): 
        """
        Get queries for each word
        """

        results = {}


        if interval != "barchasi":
            today, before = self.interval_range(interval)

            for keyword in keywords:
                results[keyword] = NewsDocument.search().sort('-posted_at').query(Q('range', posted_at={"gte":before, "lte":today}) & Q('prefix', title=keyword))

        else:
            for keyword in keywords:
                results[keyword] = NewsDocument.search().sort('-posted_at').query('prefix', title=keyword)

        return results


    def get_query(self, word, interval):

        
        if interval != "barchasi":
            today, before = self.interval_range(interval)
            results = NewsDocument.search().sort('-posted_at').query(Q('range', posted_at={"gte":before, "lte":today}) & Q('prefix', title=word))

        else:
            results = NewsDocument.search().sort('-posted_at').query('prefix', title=word)

        
        #results = News.objects.filter(Q(posted_at=today) | Q(posted_at=yesterday)).filter(title__iregex=r'\b'+str(word))
        
        return results


    
    def search(self, words, interval):


        for word in words:
            if NewsDocument.search().query('prefix', title=word).count() > 0:
                query = Q('prefix', title=word)  # empty Q object
                break
        else:
            query = Q('prefix', title=words[0])
        

        for word in words:
            if NewsDocument.search().query('prefix', title=word).count() > 0:
                temp_q = query & Q('prefix', title=word)
                if NewsDocument.search().query(temp_q).count() > 1:
                    query = temp_q


        if interval != "barchasi":
            today, before = self.interval_range(interval)
            query = query & Q('range', posted_at={"gte":before, "lte":today})

        results = NewsDocument.search().sort('-posted_at').query(query)


        return results


    def interval_range(self, state):
        today = datetime.now(pytz.timezone('Asia/Tashkent')).date()
        decrement = 1

        if state == "songilari":
            decrement = 1
        elif state == "haftalik":
            decrement = 7
        elif state == "oylik":
            decrement = 30

        before = (today-timedelta(decrement))

        return today, before

    





def index(request):

    helper = Helper()

    all_words = WatchList.objects.all()
    dic = {}
    today, before = helper.interval_range("songilari")
    option = request.session.get('interval')

    # if option == "barchasi" and not request.user.is_authenticated():
    #     return 

    if not option:
        option = 'songilari'

    for word in all_words:

        results = NewsDocument.search().query(Q('range', posted_at={"gte":before, "lte":today}) & Q('prefix', title=word.word)).count()
        if results > 2:
            results=results//2
            dic[word] = results

    if request.method == "POST":
        text = request.POST["keywords"]
        interval = request.POST["interval"]

        request.session['text'] = text

        if interval == "barchasi" and not request.user.is_authenticated:
            request.session['interval'] = "songilari"
            messages.add_message(request, messages.WARNING, "Barchasini ko'rish saytdan ro'yhatdan o'ting!")

        else:

            request.session['interval'] = interval


        return redirect('query_keywords')
        
    return render(request, 'index.html', {'dic':dic, 'option':option})





def query_keywords(request):

    helper = Helper()

    text = request.session.get('text')
    interval = request.session.get('interval')

    keywords = helper.clean_keywords(text)
    matched_news = []

    if len(keywords) > 0:
        matched_news = helper.search(keywords, interval)
    
    results = helper.get_quaries(keywords, interval)

    return render(request, 'query_keywords.html', {'results':results, 'matches':matched_news})





def query_news(request, word):

    helper = Helper()

    interval = request.session.get('interval')

    search = helper.get_query(word, interval)

    limit = settings.POSTS_PER_PAGE

    q = request.GET.get('q')
    page = int(request.GET.get('page', '1'))
    start = (page-1) * limit
    end = start + limit

    results = search[start:end].to_queryset()

    cnt=search.count()
    

    paginator = Paginator(search, limit)


    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    
    info={'word': word, 'count': cnt}

    return render(request, 'query_news.html', {'page_obj': page_obj, 'results':results, 'info': info})



def category_view(request, category):

    helper = Helper()

    # today = datetime.now(pytz.timezone('Asia/Tashkent')).date()
    # yesterday = (today-timedelta(1))

    interval = request.session.get('interval')
    today, before = helper.interval_range(interval)

    limit = settings.POSTS_PER_PAGE

    q = request.GET.get('q')
    page = int(request.GET.get('page', '1'))
    start = (page-1) * limit
    end = start + limit

    #news = News.objects.filter(Q(posted_at=today) | Q(posted_at=yesterday)).filter(category=category)
    news = NewsDocument.search().query(Q('range', posted_at={"gte":before, "lte":today}) & Q('match', category=category))
    

    paginator = Paginator(news, limit)

    results = news[start:end].to_queryset()

    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    

    cnt = news.count()
    cat = category[0].upper()+category[1:]
    info={'category':cat, 'count':cnt}

    return render(request, 'category_view.html', {'page_obj': page_obj, 'results':results, 'info': info})


@login_required
def profile(request):

    helper = Helper()

    interval = 'songilari'


    if request.is_ajax():

        id1 = request.GET.get('id', None)

        if id1:
            print(id1)

            remove_word = Keywords.objects.filter(id = id1)[0]
            if request.user in remove_word.users.all():
                remove_word.users.remove(request.user)

        else:
            usr_input = request.POST.get('keywords', None)
            raw_interval = request.POST.get('interval', None)
        
            if raw_interval:
                interval = raw_interval
                request.session['interval'] = interval


            # print(mykeys)

            if usr_input:
                words = helper.clean_keywords(usr_input)
                
                for item in words:

                    cur_word = Keywords.objects.get_or_create(word = item)[0]

                    if not request.user in cur_word.users.all():
                        cur_word.users.add(request.user)


        
                    
        rawwords = Keywords.objects.filter(users=request.user)
    
        mywords = []

        keywords = [word.word for word in rawwords]

        matched_news = []

        count_words = {}

        for item in helper.search(keywords, interval):
            
            d = {'title': item.title,
                    'link': item.link,
                    'views': item.views,
                    'category': item.category,
                    'posted_at': item.posted_at.strftime("%d %b %y"),
                    'source': item.source}
            matched_news.append(d)

        # print(keywords)


        result = {}

        for keyword in rawwords:
            res = helper.get_query(keyword.word, interval)

            count_words[keyword.word] = res.count()

            mywords.append({'word':keyword.word, 
                            'id':keyword.id})
            
            lak = []
            for item in res:
                d = {'title': item.title,
                     'link': item.link,
                     'views': item.views,
                     'category': item.category,
                     'posted_at': item.posted_at.strftime("%d %b %y"),
                     'source': item.source}
                lak.append(d)

            result[keyword.word] = lak



        response = {'words':mywords, 'news':result, 'matches':matched_news, 'keywords':keywords, 'count_words':count_words}
        
        return JsonResponse(response)
    


    return render(request, 'profile.html')


def error_404_view(request, exception):
    return render(request,'404.html')


class FilterView(ListView):
    model = WaitList
    template_name = 'filter.html'
    context_object_name = 'words'
    paginate_by = 200
    


class DirectWord(View):
    def  get(self, request):

        id1 = request.GET.get('id', None)
        text = request.GET.get('text', None)

        # print(text)

        word = WaitList.objects.get(id=id1).word

        if text=="accept":
            if not WatchList.objects.filter(word=word).exists():
                tag = WatchList(word = word)
                tag.save()

        else:
            if not IgnoreList.objects.filter(word=word).exists():
                tag = IgnoreList(word = word)
                tag.save()

        WaitList.objects.get(id=id1).delete()

        data = {
            'deleted': True
        }
        return JsonResponse(data)




from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import (
    NotTelegramDataError, 
    TelegramDataIsOutdatedError,
)

bot_name = settings.TELEGRAM_BOT_NAME
bot_token = settings.TELEGRAM_BOT_TOKEN
redirect_url = settings.TELEGRAM_LOGIN_REDIRECT_URL



def authenticate_user(request):

    if request.GET.get('hash'):
    
        try:
            result = verify_telegram_authentication(bot_token=bot_token, request_data=request.GET)

            new_username = result['id']
            new_first_name = result['first_name']
            new_last_name = ""
            new_telegram_username = ""
            
            if 'last_name' in result:
                new_last_name = result['last_name']

            if 'username' in result:
                new_telegram_username = result['username']


            if not User.objects.filter(username=new_username).exists():
                user = User.objects.create_user(username=new_username, telegram_name=new_telegram_username, first_name=new_first_name, last_name=new_last_name)
                
            
            else:
                
                user = User.objects.get(username=new_username)

            user.backend = 'django.contrib.auth.backends.ModelBackend'

            if user is not None:    

                login(request, user)

                return redirect('profile')
            else:

                return HttpResponse("Error creating user!")

        except TelegramDataIsOutdatedError:
            return HttpResponse('Authentication was received more than a day ago.')

        except NotTelegramDataError:
            return HttpResponse('The data is not related to Telegram!')


    raise Http404('Bad Request!')
