#!/usr/bin/python
from features import data
from features import notification
from os.path import join, dirname
from dotenv import load_dotenv

def main():
    users_import = data.Users(
        file = './datas/users.csv'
    )
    users = users_import._import()

    for user in users:
        email = user.split(',')[0]
        language = user.split(',')[1]
        country = user.split(',')[2]
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
            recipient = email
            message = data_news
        )
        mail.send()

if __name__ == "__main__":
    dotenv_path = join(dirname(__file__), './datas/.env')
    load_dotenv(dotenv_path)
    NEWS_API_KEY = os.getenv('news_api_key')
    SMTP_SERVER = os.getenv('smtp_server')
    SMTP_PORT = os.getenv('smtp_port')
    SMTP_USERNAME = os.getenv('smtp_username')
    SMTP_PASSWORD = os.getenv('smtp_password')
    main()