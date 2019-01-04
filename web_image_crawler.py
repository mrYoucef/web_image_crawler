
import os
import requests
from bs4 import BeautifulSoup



def download_web_image(url):

    file_name = url.split('/')[-2] + '_' + url.split('/')[-1]
    if not os.path.isfile('img//' + file_name):
        r = requests.get(url, allow_redirects=True)
        open('img//' + file_name, 'wb').write(r.content)


def page_image_crawler(url,type='img',type2='src'):
        html_respond = requests.get(url)
        plain_text = html_respond.text
        soup = BeautifulSoup(plain_text, features="html.parser")
        for link in soup.findAll(type):
            href = link.get(type2)
            if (str(href).split('//')[0] == 'https:' ) or (str(href).split('//')[0] == 'http:'):
                try:
                    download_web_image(href)
                    print(href)
                except:
                    pass
            else :
                try:
                    download_web_image(url + href)
                    print(url + href)
                except:
                   pass


def web_image_crawler(url, max): #max is to specify the depth of crawling

    try:
        try:
            page_image_crawler(url)
        except:
            pass
        if max > 0:
            html_respond = requests.get(url)
            plain_text = html_respond.text
            soup = BeautifulSoup(plain_text, features="html.parser")
            for link in soup.findAll('a'):
                href = link.get('href')
                if (str(href).split('//')[0] == 'https:' ) or (str(href).split('//')[0] == 'http:'):
                    try:
                        page_image_crawler(href)
                    except:
                        pass
                else :
                    try:
                        page_image_crawler(url + href)
                    except:
                       pass
                if (str(href).split('//')[0] == 'https:') or (str(href).split('//')[0] == 'http:'):
                    try:
                        web_image_crawler(href, max-1)
                    except:
                        pass
                else:
                    try:
                        web_image_crawler(url + href, max-1)
                    except:
                        pass
    except:
        pass #



url = r"http://www.fliptext.org/"

if not os.path.exists('img//'):
    os.makedirs('img//')


web_image_crawler(url, 1)
