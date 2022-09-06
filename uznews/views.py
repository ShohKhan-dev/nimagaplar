
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from uznews.models import *

from django.views.generic import ListView, View
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator

from datetime import datetime, timedelta
import pytz
from django.contrib.admin.views.decorators import staff_member_required
# from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
import re

from django.db.models import Q
from django.contrib.auth import authenticate, login


# Create your views here.

# from .documents import NewsDocument


# s = NewsDocument.search().query("match", title="andijon")

# for hit in s:
#     print(
#         "results: ", hit.title
#     )


def search(words):

    matched_words = []

    

    
    query = Q(title__icontains=words[0])  # empty Q object

    for word in words:
        
        # 'or' the queries together
        if News.objects.filter(title__icontains=word).exists():
            temp_q = query & Q(title__icontains=word)

            if News.objects.filter(temp_q).count() > 0:
                query = temp_q
                matched_words.append(word)
            
    
            print(Q(title__icontains=word))

        

    results = News.objects.filter(query).all()


    return results



def get_query(word):
    today = datetime.now(pytz.timezone('Asia/Tashkent')).date()
    yesterday = (today-timedelta(1))
    results = News.objects.filter(Q(posted_at=today) | Q(posted_at=yesterday)).filter(title__iregex=r'\b'+str(word))
    
    return results



def clean_keywords(text):

    text = text.replace(",", " ").lower()

    text = re.sub("[^a-zA-Z' ]+", "", text)
    
    keywords = [word.strip().replace("'", "‘") for word in text.split()]

    return keywords
        




def get_quaries(keywords):

    results = {}


    for keyword in keywords:
        res = get_query(keyword)
        results[keyword] = res

    return results





def index(request):



    all_words = WatchList.objects.all()
    dic = {}

    today = datetime.now(pytz.timezone('Asia/Tashkent')).date()
    yesterday = (today-timedelta(1))

    for word in all_words:
        results = News.objects.filter(Q(posted_at=today) | Q(posted_at=yesterday)).filter(title__iregex=r'\b'+str(word)).count()
        if results > 4:
            results=results//2
            dic[word] = results

    

    if request.method == "POST":
        test = request.POST["keywords"]


        request.session['text'] = test

        return redirect('query_keywords')
        
    return render(request, 'index.html', {'dic':dic})





def query_keywords(request):

    text = request.session.get('text')

    keywords = clean_keywords(text)

    matched_news = []

    if len(keywords) > 0:
        matched_news = search(keywords)
    

    results = get_quaries(keywords)

    return render(request, 'query_keywords.html', {'results':results, 'matches':matched_news})





def query_news(request, word):

    results = get_query(word)


    cnt=results.count()

    paginator = Paginator(results, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    info={'word': word, 'count': cnt}

    return render(request, 'query_news.html', {'page_obj': page_obj, 'info': info})




def category_view(request, category):

    today = datetime.now(pytz.timezone('Asia/Tashkent')).date()
    yesterday = (today-timedelta(1))

    news = News.objects.filter(Q(posted_at=today) | Q(posted_at=yesterday)).filter(category=category)
    cnt = news.count()

    paginator = Paginator(news, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cat = category[0].upper()+category[1:]

    info={'category':cat, 'count':cnt}

    return render(request, 'category_view.html', {'page_obj': page_obj, 'info': info})


@login_required
def profile(request):

    if request.is_ajax():

        id1 = request.GET.get('id', None)

        if id1:
            print(id1)

            remove_word = Keywords.objects.filter(id = id1)[0]
            if request.user in remove_word.users.all():
                remove_word.users.remove(request.user)

        else:
            usr_input = request.POST.get('keywords', None) 
            print(usr_input)

            mykeys = Keywords.objects.all()

            print(mykeys)

            if usr_input:
                words = clean_keywords(usr_input)
                
                for item in words:

                    cur_word = Keywords.objects.get_or_create(word = item)[0]

                    if not request.user in cur_word.users.all():
                        cur_word.users.add(request.user)
                    
        rawwords = Keywords.objects.filter(users=request.user)
    
        mywords = []

        keywords = [word.word for word in rawwords]

        matched_news = []

        for item in search(keywords):
            d = {'title': item.title,
                    'link': item.link,
                    'views': item.views,
                    'category': item.category,
                    'posted_at': item.posted_at,
                    'source': item.source}
            matched_news.append(d)

        print(keywords)


        result = {}

        for keyword in keywords:
            res = get_query(keyword)
            lak = []
            for item in res:
                d = {'title': item.title,
                     'link': item.link,
                     'views': item.views,
                     'category': item.category,
                     'posted_at': item.posted_at,
                     'source': item.source}
                lak.append(d)

            result[keyword] = lak

        
        for item in rawwords:
            mywords.append({'word':item.word, 
                            'id':item.id})

        response = {'words':mywords, 'news':result, 'matches':matched_news, 'keywords':keywords}
        
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
