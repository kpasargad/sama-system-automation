# -*- coding: utf-8 -*-
from requests import session
import hashlib
from bs4 import BeautifulSoup
import smtplib
import email.mime.text

loginPayload = {
    'action': 'login',
    'UserType': 'Student',
    'UserCode': '921221115',
    'KeyCode': hashlib.md5("1272010716").hexdigest()
}

with session() as c:
    c.post('http://vce.umz.ac.ir/samaweb/login.asp', data=loginPayload)
    response = c.get('http://vce.umz.ac.ir/samaweb/LessonReport.asp')
    # print(response.headers)
    # print(response.text)

searchPayload = {
    'LessonType': '0',
    'Completed': 'NotComplete',
    'Search': 'LessonCodeSelect',
    'SearchPattern': '2120032',
    'PageNum': '1',
}

result = c.request("post",
                   "http://vce.umz.ac.ir/samaweb/LessonReport.asp",
                   data=searchPayload, cookies=response.cookies).text

# print result


soup = BeautifulSoup(result, 'html.parser')
stuff = soup.find_all('span')
flag = 0

for span in stuff:
    # print str(span.contents)
    if flag == 1:
        capacity = str(span.contents)[3:-2]
        message = "ظرفیت باقیمانده درس مورد نظر: " + capacity
        print message
        flag = 0
    if str(span.contents) == "[u'\u0628\u0627\u0642\u064a\u0645\u0627\u0646\u062f\u0647: ']":
        flag = 1

if capacity>0:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("kpasargad2@gmail.com", "itjki]hvnisi")
    msg = email.mime.text.MIMEText(message, _charset="UTF-8")
    server.sendmail("kpasargad2@gmail.com", "kpasargad2@gmail.com", msg.as_string())
    server.quit()
