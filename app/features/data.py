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
                    output = ""
                    for art in headlines:
                        output += f"Title: {art['title']}\nDescription: {art['description']}\nURL: {art['url']}\n -----\n"
                    return output
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
                output = ""
                for fact in chosen_facts:
                    output += f"{fact}\n"
                output += " -----"
                return output
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
        output = ""
        for elem in self.message:
            output += "**********"
            output += f"{elem}\n"
        output += "**********"
        return output