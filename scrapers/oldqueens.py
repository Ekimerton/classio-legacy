import requests
import os

print("started")
with requests.Session() as c:

    # Queen's requires login to view classes (wtf)
    username = os.environ['QUEENS_USERNAME']
    password = os.environ['QUEENS_PASSWORD']
    login_data = dict(j_username=username, j_password=password)

    login_url = "https://my.queensu.ca/c/portal/login"
    c.get(login_url)
    post = c.post(login_url, data=login_data, headers={"Referer": "https://login.queensu.ca/idp/profile/SAML2/Redirect/SSO?execution=e1s2"})
    print(post.url)
    login = c.post(post.url)
    print(login.content)

    #c.post(login_url, data=login_data)

print("ended")
