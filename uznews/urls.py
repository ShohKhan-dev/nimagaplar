from django.urls import path
from .views import *
from . import views

from django.contrib.auth import views as vi


urlpatterns = [
    path("", views.index, name="index"),

    path('keywords/',query_keywords, name='query_keywords'),
    


    path('news/<str:word>/', query_news, name='query_news'),

    path('category/<str:category>/', category_view, name='category_view'),

    path('profile/', profile, name='profile'),

    path('authenticate/', authenticate_user, name='authenticate'),

    path('logout/', vi.LogoutView.as_view(), name='logout'),

]