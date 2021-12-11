import requests
from requests.sessions import Session
from bs4 import BeautifulSoup
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
        
    
    def login(self):
        """Logins to AFB and return session"""
        URL = 'https://www.afbostader.se/'
        s = requests.Session()
        #s.get(URL)
        s.post(URL, data=self.data)
        return s


def availableDates(s, token):
    params = (
        ('Token', token),
        ('DateFrom', '2021-12-07'),
        ('DateTo', '2022-01-14'),
        ('Groups', '16'),
    )
    response = s.get('https://aptusbookingservice.afbostader.se/bookingservice.svc/GetCalendarData', params=params)
    js = response.json()

    i = 0
    for day in js['Days']:
        passes = day['DayGroups'][0]['BookablePasses']
        if passes:
            for time in passes:
                
                if time['No'] == 4:
                    print(day['Date'])

def getToken(s):
    """Return the unique token. Required to make call to booking service"""
    URL = 'https://www.afbostader.se/dina/sidor/boka-bastu/'
    r = s.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        value = soup.find('input', {'id': 'hidAptusToken'}).get('value')
        return value
    except Exception as e:
        print("Got unhandled exception %s" % str(e))


if __name__ == "__main__":
    # Generates data
    Py = Account('EMAIL', 'PASS')
    #  Logins to AFB and return session
    s = Py.login()
    token = getToken(s)

    
    availableDates(s, token)
    
        