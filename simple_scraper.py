import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = 'https://www.amazon.ca/Netac-Rotated-External-Storage-Digital/dp/B083DKWT3Y/ref=sr_1_8?dchild=1&keywords=usb+256gb&qid=1617433479&sr=8-8'


headers = { "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36', "Pragma": "no-cache"}
budget = int(input("What is your budget? "))
MyEmail = str(input("Enter your email? "))
MyPassword = str(input("Enter your app password? "))


def check_price():
    page = requests.get(URL,headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    title = title.strip()

    price = soup.find(id="priceblock_saleprice").get_text() #normal price
    if price is None:
        price = soup.find(id="priceblock_ourprice").get_text() #discount
    converted_price = get_converted_price(price)
    float_price = float(converted_price)

    if (float_price <= budget):
        send_email()

def get_converted_price(price):

    converted_price = price.replace("CDN$", "")
    return converted_price


def send_email():

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(MyEmail, MyPassword)

        subject = 'Price fell down!'
        body = "Follow the link at " + URL

        msg = f"Subject: {subject}\n\n{body}"


        server.sendmail(MyEmail, MyEmail, msg)
        server.close()
        print('Email has been sent')


    except:
        print('Something went wrong...')
        server.quit()


while True:
    check_price()
    time.sleep(3600)