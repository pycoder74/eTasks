from bs4 import BeautifulSoup
import requests

url = 'https://github.com/pycoder74/eTasks'
ext = 'iso'

def listFD(url, ext=''):
    page = requests.get(url, verify = False).text
    soup = BeautifulSoup(page, 'html.parser')
    return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
directories =listFD(url)
list = []
for i in directories:
    list.append(i)
num = 0
for index, item in enumerate(list):
    print(list[index]))
    num = num + 1
    
