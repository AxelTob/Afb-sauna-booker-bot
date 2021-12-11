import gmail
import requests
from requests.sessions import Session
import time
from schedule import * 
import schedule
from bs4 import BeautifulSoup
import datetime

class Account:
    
    def __init__(self, email, password) -> None:
        self.data =  {
  '__EVENTTARGET': '',
  '__EVENTARGUMENT': '',
  '__VIEWSTATE': '/wEPDwULLTE5MDAyODUwODVkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYCBSZjdGwwMCRjdGwyNSRMb2dpbkNvbnRyb2wkY2hrUmVtZW1iZXJNZQUmY3RsMDAkY3RsMjkkTG9naW5Db250cm9sJGNoa1JlbWVtYmVyTWUZC98b4Wwj+A0yAHw7ORlJC6N5MiZF0Jk+og9XZhqO2Q==',
  '__VIEWSTATEGENERATOR': '9345F2A8',
  '__EVENTVALIDATION': '/wEdAAwi5TmzpFG20Bu/GVe0HTOXzEHg9XOOFTnaRtup/xN2H9zfwMl9EJOElzCIu+jVJcNexydOMEOC3vxuYK/isGajffL4wvHcA8wDB9JCE0Dlxt0Bx0snz+eAxawA+B7rJmaqh4CFgckOjI3+8lIGmcRXgBKFdOsEIcs0nlYwFTfYc1ZA0XjABxVFI7uJutt2Io+xXxdkTh3DRDBznH5YqwmCTy+YXLFP1ReFt07ABaFBD7Owkpln17nCtQ6PDLIMK1P7/5CQ+iU/hx7zIv9sdahNYh84edgLg0J9b8Ku3j48Kg==',
  'ctl00$ctl25$LoginControl$UserName': email,
  'ctl00$ctl25$LoginControl$Password': password,
  'ctl00$ctl25$LoginControl$btnLogIn': 'Logga in',
  'ctl00$ctl26$hidSearchUrl': 'https://www.afbostader.se/sok/',
  'fake_chrome_username': '',
  'fake_chrome_password': '',
  'q': '',
  'quicksearch': '',
  'ctl00$ctl29$LoginControl$UserName': '',
  'ctl00$ctl29$LoginControl$Password': '',
  'ctl00$ctl29$LoginControl$email_reset': ''
}
        
    
    def login(self) -> Session:
        s = requests.Session()
        s = requests.get('https://www.afbostader.se/')
        s.post('https://www.afbostader.se/', data=self.data)
        return s

def getCurrentDateTime():
    t = datetime.datetime().now().date()
    date = t.strftime('%y-%m-%d')
    return date + 'T19:00'

def tryBook(s, token):

    params = (
    ('Token', token),
    ('StartTimestamp', getCurrentDateTime()),
    ('LengthMinutes', '180'),
    ('GroupId', '16'),
    ('MaxWaitSeconds', '60'),
)

    response = s.get('https://aptusbookingservice.afbostader.se/bookingservice.svc/Book', params=params)
    print(response.json())
    try:
        if response.json()['UnBookable']:
            print('success')
            
    except:
        print('Lets try again tomorrow')
        

def getToken(s):
    URL = 'https://www.afbostader.se/dina/sidor/boka-bastu/'
    r = s.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        value = soup.find('input', {'id': 'hidAptusToken'}).get('value')
        print(value)
        return value
    except Exception as e:
        print("Got unhandled exception %s" % str(e))
    #mydivs = soup.find_all("div", {"class": "price-ticket__fluctuations"})

def main():
    print('called')
    # generate data - PUT EMAIL AND PASSWORD HERE for afb
    Py = Account('EMAIL', 'PASSWORD')
    #  Logins to AFB and return session
    s = Py.login()
    # fetch token
    token = getToken(s)
    # try book, check if it's available.
    tryBook(s, token)


#def notifyy():
    #gm = gmail()
    #gm.notify()

if __name__ == "__main__":
    
    #schedule everyday - 1min margin
    schedule.every().day.at("19.30").do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
    
    
        