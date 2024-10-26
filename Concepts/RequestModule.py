# The python Request module  is used to send HTTP requests.
# It can be installed using pip install request package

# import requests
# from bs4 import BeautifulSoup


# GET REQUEST -----
from bs4 import BeautifulSoup # type: ignore
import requests # type: ignore
response = requests.get("https://www.apple.com")
print(response.text)


# bs4 MODULE ---- BEAUTIFUL MODULE  SCRAPING TOOLKIT

# from bs4 import BeautifulSoup
# soup = BeautifulSoup(response.content, 'html.parser')

url = "https://www.codewithharry.com/blogpost/django-cheatsheet/"
r = requests.get(url)
# print(r.text)


soup = BeautifulSoup(r.text, 'html.parser')
print(soup.prettify())
for heading in soup.find_all("h2"):
    print(heading.text)

#IMP CONCEPT!!!!!