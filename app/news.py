#!/usr/bin/python
from features import data
from features import notification
from path import join, dirname
from os import getenv
from dotenv import load_dotenv

def main():
    users_import = data.Users(
        file = './datas/users.csv'
    )
    users = users_import._import()

    for user in users:
        email = user[0]
        language = user[1]
        country = user[2]
        news = data.RetrieveData(
            api_key = NEWS_API_KEY,
            language = language,
            country = country
        )
        data_news = news.extract()
        news = data.PrepareNotification(
            message = data_news
        )
        data_news = news.run()
        mail = notification.MailNotification(
            SMTPServer = SMTP_SERVER,
            SMTPPort = SMTP_PORT,
            SMTPUsername = SMTP_USERNAME,
            SMTPPassword = SMTP_PASSWORD,
            recipient = email,
            message = data_news
        )
        mail.send()

if __name__ == "__main__":
    dotenv_path = join(dirname(__file__), './datas/.env')
    load_dotenv(dotenv_path)
    NEWS_API_KEY = getenv('news_api_key')
    SMTP_SERVER = getenv('smtp_server')
    SMTP_PORT = getenv('smtp_port')
    SMTP_USERNAME = getenv('smtp_username')
    SMTP_PASSWORD = getenv('smtp_password')
    main()