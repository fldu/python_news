#!/usr/bin/python

from newsapi import NewsApiClient
from bs4 import BeautifulSoup
import time
import logging
import requests
import random
import csv 

logging.basicConfig(level=logging.INFO, filename='debug.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%y-%m-%dT%H:%M:%S%z')

class Users:
    def __init__(
        self,
        file
    ):
        self.file = file
    
    def _import(self):
        try:
            with open(self.file) as f:
                reader = csv.reader(f)
                output = list(reader)
                return output
        except Exception as e:
            logging.warning(f"User import error: {e}")
            return False

class RetrieveData:
    def __init__(
        self,
        api_key,
        language,
        country,
    ):
        self.api_key = api_key
        self.language = language
        self.country = country

    def extract(self):

        def retrieve_from_newsApi(self):
            try:
                newsapi = NewsApiClient(api_key = self.api_key)
                try:
                    headlines = newsapi.get_top_headlines(
                        language = self.language,
                        country = self.country
                    )
                    headlines = headlines['articles']
                    news = []
                    for art in headlines:
                        news.append([art['title'],art['description'],art['url'], art['urlToImage']])
                    dict_news = {
                        'module_title': "News",
                        'data': news
                    }
                    return dict_news
                except Exception as e:
                    logging.warning(f"Exception in downloading the news: {e}")
                    return False
            except Exception as e:
                logging.warning(f"Exception in creation of the news api client: {e}")
                return False

        def retrieve_fun_fact_of_the_day(self):
            today = time.strftime("%B_%d")
            try:
                r = requests.get(f"https://en.wikipedia.org/wiki/{today}")
                soup = BeautifulSoup(r.text, "html.parser")
                facts = soup.find_all('ul')[1].text
                facts = facts.split('\n')
                chosen_facts = random.choices(facts, k=5)
                dict_facts = {
                    'module_title': 'Fun facts of the day',
                    'data': chosen_facts
                }
                return dict_facts
            except Exception as e:
                logging.warning(f"Exception in retrieving wikipedia page: {e}")
                return False

        news = retrieve_from_newsApi(self)
        fun_fact = retrieve_fun_fact_of_the_day(self)
        return [news, fun_fact]

class PrepareNotification:

    def __init__(
        self,
        message
    ):
        self.message = message

    def run(self):
        #Greetings
        today = time.strftime("%A %d %B %Y")
        output = ""
        output += """
<html>
<head>
        <style>
            body{
                background: #ededed;
                margin: 0 auto;
            }
            .listing {
            padding: 0;
            margin: 0;
            width: 100%;
            border-bottom: 0;
            }
            .listing li{
                width: 100%;
                float: none;
                border: none;
                margin: 2px;
                padding: 10px;
                text-align: left;
                height: 120px;
            }
        </style>
</head>
        """
        output += f"<body><h2>Good morning, today is {today}</h2>"
        #News module here
        title = self.message[0]['module_title']
        data = self.message[0]['data']
        output += f'<h2> {title}: </h2><ul class=listing style="list-style: none">'
        for elem in data:
            news_title = elem[0]
            news_desc = elem[1]
            news_link = elem[2]
            news_img = elem[3]
            output += f'<li><img style="float: left;" src="{news_img}" alt="image" height="100" /> <a style="margin-left: 5px;" href={news_link}>{news_title}</a><p style="margin-left: 5px;">{news_desc}</p></li>'
        output += "</ul>"
        #Wikipedia fact
        title = self.message[1]['module_title']
        data = self.message[1]['data']
        output += f"<h2> {title}: </h2>"
        for elem in data:
            output += f'<p style="margin-left: 5px;">{elem}</p>'
        #Wish a good day
        output += "<h2>Have a good day!<h2>"
        output += "</html>"
        return output