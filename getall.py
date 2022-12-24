import requests
from bs4 import BeautifulSoup
import json
import pytz
import re
from datetime import datetime

import os
import django


os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()

from uznews.models import WaitList, WatchList, IgnoreList, News

class GetAll():

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.news_list = []


    def kun_uz(self):

        is_new = True
        page = 1

        kun_news = []

        stop_point = "uz/news/1970/01/01/mediapark-ustozlarga-rahmat-bayram-aksiyasiga-start-berdi"


        while is_new:

            try:
                url = "https://m.kun.uz/uz?q=%2Fuz&page=" + str(page)
    
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text,'html.parser')
                news = soup.find("div", class_="col-xs-12")


                for item in news.find_all('div', class_="post-body"):

                    main = item.find('a', class_="post-title")
                    lk = main.get('href')[1:]
                    date = lk[8:18]
                    # print(date)

                    link = lk
                    title = main.text.strip()
                    views = item.find('span', class_="viewed").text
                    category= item.find('a', class_="float-none blue").text.strip()

                    if category == "O‘zbekiston":
                        category = "mahalliy"
                    elif category == "Jahon":
                        category = "dunyo"
                    elif category == "Jamiyat":
                        category = "jamiyat"
                    elif category == "Sport":
                        category = "sport"
                    elif category == "Iqtisodiyot":
                        category = "iqtisodiyot"
                    elif category == "Fan va texnika":
                        category = "texnalogiyalar"
                    elif category == "Light":
                        category = "lifestyle"
                    else:
                        category = "lifestyle"


                
                    kun_news.append(list((title, link, views, category, date, "kun.uz")))

                
                    # my_d["title"] = title
                    # my_d["link"] = link
                    # my_d["views"] = views
                    # my_d["category"] = category
                    # my_d["date"] = date
                    # my_d["source"] = "kun.uz"



                    if link == stop_point:
                        is_new = False
                        break
                
                page+=1

            except Exception as e:
                print(e)
                print("stopped on page: ",page)
                break

        return kun_news

    def daryo_uz(self):
    
        categories = ["mahalliy", "dunyo", "texnologiyalar", "madaniyat", "avto", "sport", "foto", "lifestyle"]
        daryo_news = []

        for category in categories:
            page = 1

            while True:

                try:

                    url = "https://admin.daryo.uz/category/"+ category +"/page/"+str(page)+"/"

                    response = requests.get(url, headers = self.headers)
                    

                    if response.status_code != 200:
                        break
                
                    soup = BeautifulSoup(response.text,'html.parser')
                    news = soup.find("div", class_="main")

                    for article in news.find_all("article", class_="cat_article"):

                        main = article.find("a")
                        lk = main.get('href')[23:]
                        date = lk[:10]
                        
                        link=lk
                        title = main.text
                        views = article.find('span', class_="meta_views").text.replace(" ", "")

                        daryo_news.append(list((title, link, views, category, date, "daryo.uz")))

                        # my_d["title"] = title
                        # my_d["link"] = link
                        # my_d["views"] = views
                        # my_d["category"] = category
                        # my_d["date"] = date
                        # my_d["source"] = "daryo.uz"


                
                    page+=1
                
                except Exception as e:
                    print(e)
                    print("stopped on: ", category, 'page: ', page)
                    break

        
        return daryo_news



    # def store_json(self):
        
    #     with open("mydata.json", "w", encoding="utf-8") as final:
    #         json.dump(self.news_list, final)

    # def read_josn(self):
    #     with open("mydata.json", "r") as read_file:
    #         data = json.load(read_file)
    #     print(data)

    
    def write_data(self, all_news):

        new_added_news = []

        for news in all_news:
            title = news[0]

            title = title.replace("‘", "'")
            title = title.replace("—", "-")
            title = title.replace("“", "''")
            title = title.replace("”", "''")
            
            link = news[1]
            views = int(news[2])
            category = news[3]
            posted_at = datetime.strptime(news[4], '%Y/%m/%d').date()
            source = news[5]

            if not News.objects.filter(link=link).exists():
                data = News(title = title, link = link, views = views, category=category, posted_at = posted_at,  source = source)
                data.save()

                new_added_news.append(data)


        print("news are added!", len(new_added_news))



    def run(self):
        kun_news = self.kun_uz()

        print("All Kun uz news: ", len(kun_news))

        self.write_data(kun_news)


        daryo_news = self.daryo_uz()

        print("All Daryo uz news: ", len(daryo_news))

        self.write_data(daryo_news)

    



getall = GetAll()

getall.run()

# getall.kun_uz()
# getall.daryo_uz()
# getall.store_json()
# getall.print_size()
# getall.read_josn()