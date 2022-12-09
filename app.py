import smtplib
import requests
import os
# from keys import vars

from calendar import monthrange
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


available_dates = ['h']


def make_request(year,month,day):
    api_key = os.environ['api_key']
    venue_id = os.environ['venue_id']
    
    url = f"https://api.resy.com/4/find?lat=45.5152&long=-122.6784&day={year}-{month}-{day}&party_size=2&venue_id={venue_id}"

    payload = ""
    headers = {
    'Authorization': f"ResyAPI api_key={api_key}"
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data=response.json()
    print(month,day)
    try:
        current_opening = data['results']['venues'][0]['slots'][0]['shift']['day']
        print('CURRENT OPENING', data['results']['venues'][0]['slots'][0] )
        available_dates.append(current_opening)
    except: 
        print("No openings")
        

def find_reservation():
    counter = 0
    while counter < 2:
        current_month =  date.today() + relativedelta(months=+counter)
        month_to_integer = int(current_month.strftime("%m"))
        current_year = datetime.now().year + counter
        days_in_month = monthrange(current_year, month_to_integer)[1]
        for day in range(days_in_month+1):
            make_request(current_year,month_to_integer,day)
        counter +=1

def send_mail():
    email = os.environ['email']
    email_password = os.environ['email_password']

    sent_from = email
    to = [email, email]
    subject = 'Lorem ipsum dolor sit amet'
    body = " ".join(available_dates)

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(email, email_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)

find_reservation()
if available_dates:
    send_mail()
