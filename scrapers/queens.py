import requests
import os

print("started")
with requests.Session() as c:

    # Queen's requires login to view classes (wtf)
    username = os.environ['QUEENS_USERNAME']
    password = os.environ['QUEENS_PASSWORD']
    login_data = dict(j_username=username, j_password=password)

    url = "https://my.queensu.ca"
    page = c.post(url, continue_data)
    print(page.content)

    #c.post(login_url, data=login_data)

print("ended")
