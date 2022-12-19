from matplotlib.pyplot import get
import requests
from bs4 import BeautifulSoup
import json


class GetAll():

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.news_list = []


    def kun_uz(self):

        is_new = True
        page = 1

        stop_point = "uz/news/1970/01/01/mediapark-ustozlarga-rahmat-bayram-aksiyasiga-start-berdi"


        while is_new:

            url = "https://m.kun.uz/uz?q=%2Fuz&page=" + str(page)
    
            response = requests.get(url, headers = self.headers)
            soup = BeautifulSoup(response.text,'html.parser')
            news = soup.find("div", class_="col-xs-12")


            for item in news.find_all('div', class_="post-body"):
                my_d = {}

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

                

            
                my_d["title"] = title
                my_d["link"] = link
                my_d["views"] = views
                my_d["category"] = category
                my_d["date"] = date
                my_d["source"] = "kun.uz"

                self.news_list.append(my_d)

                if link == stop_point:
                    is_new = False
                    break
            
            page+=1

    def daryo_uz(self):
    
        categories = ["mahalliy", "dunyo", "texnologiyalar", "madaniyat", "avto", "sport", "foto", "lifestyle"]

        for category in categories:
            page = 1

            while True:

                url = "https://admin.daryo.uz/category/"+ category +"/page/"+str(page)+"/"

                response = requests.get(url, headers = self.headers)
                

                if response.status_code != 200:
                    break
            
                soup = BeautifulSoup(response.text,'html.parser')
                news = soup.find("div", class_="main")

                for article in news.find_all("article", class_="cat_article"):
                    my_d = {}

                    main = article.find("a")
                    lk = main.get('href')[23:]
                    date = lk[:10]
                    
                    link=lk
                    title = main.text
                    views = article.find('span', class_="meta_views").text.replace(" ", "")

                    my_d["title"] = title
                    my_d["link"] = link
                    my_d["views"] = views
                    my_d["category"] = category
                    my_d["date"] = date
                    my_d["source"] = "daryo.uz"

                    self.news_list.append(my_d)

            
                page+=1



    def store_json(self):
        
        with open("mydata.json", "w", encoding="utf-8") as final:
            json.dump(self.news_list, final)

    def read_josn(self):
        with open("mydata.json", "r") as read_file:
            data = json.load(read_file)
        print(data)


        
    def print_data(self):
        print(self.news_list)

    def print_size(self):
        print(len(self.news_list))
    




getall = GetAll()

getall.kun_uz()
getall.daryo_uz()
getall.store_json()
getall.print_size()
# getall.read_josn()