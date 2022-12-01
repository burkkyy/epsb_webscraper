import os
import requests as re
from bs4 import BeautifulSoup as bs

HTTP_SUCCESS = 200

url = 'https://www.epsb.ca/'
school_list_url = url + 'schools/findaschool/list/'
html = 'data/epsb.html'
school_list_file = 'data/school_list.txt'
images = 'img/'

def download_html(url, filename):
    req = re.get(url, stream=True)
    req.raise_for_status()
    print(f"Writing data collected from {url[12:]} to {filename}")
    with open(filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size=50000):
            f.write(chunk)

def parse_html_for_links(read, write):
    with open(read, 'r') as f:
        contents = f.read()
        soup = bs(contents, 'html.parser')

    div = soup.find('ul', class_="school-list")
    with open(write, "w") as f:
        for d in div:
            _url = url + d.find('a', href=True)['href']
            req = re.get(_url, timeout=5)
            if req.status_code != HTTP_SUCCESS:
                print(f"[ERROR] timeout on link {_url}")
                continue

            s = bs(req.content, 'html.parser')
            _d = s.find('div', class_='school-left-column')
            if _d:
                f.write(_d.find_all('a', href=True)[2]['href'])
                f.write('\n')
                f.flush()
                print(_d.find_all('a', href=True)[2]['href'])
            else:
                print(f"[ERROR] with {d}")

def download_images_from_links():
    

if __name__ == '__main__':
    if(os.path.exists(html)): print("[STATUS] download_html is already done")
    else: download_html(school_list_url, html)
    if(os.path.exists(school_list_file)): print("[STATUS] parse_html_for_links is already done")
    else: parse_html_for_links(html, school_list_file)
    if(os.path.exists(images)): print("[STATUS] download_images_from_links is already done")
    else: download_images_from_links()
