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
    print(f"\033[91m[STATUS]\033[0m Writing data collected from {url[12:]} to {filename}")
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
                print(f"\033[91m[ERROR]\033[0m timeout on link {_url}")
                continue

            s = bs(req.content, 'html.parser')
            _d = s.find('div', class_='school-left-column')
            if _d:
                f.write(_d.find_all('a', href=True)[2]['href'])
                f.write('\n')
                f.flush()
                print(_d.find_all('a', href=True)[2]['href'])
            else:
                print(f"\033[91m[ERROR]\033[0m with {d}")

def download_images_from_links(url_list, out_folder):
    try:
        os.mkdir(out_folder)
    except FileExistsError:
        pass
    
    img_count = 0
    with open(url_list, 'r') as f:
        for _url in f:
            img_file_name = images + _url[8:].split('.')[0] + '.png'
            if(os.path.exists(img_file_name)):
                print(f"\033[94m[STATUS]\033[0m {img_file_name} already exists")
                continue

            try:
                req = re.get(_url[:-1], timeout=5)
                if req.status_code != HTTP_SUCCESS:
                    print(f"\033[91m[ERROR]\033[0m timeout on link {_url[:-1]}")
                    continue
            except re.exceptions.ConnectionError:
                print(f"\033[91m[ERROR]\033[0m failed to connect to {_url[:-1]}")
                continue
            
            try:
                s = bs(req.content, 'html.parser')
                for i in s.find_all('img'):
                    if(i['alt'].lower() == 'school logo'):
                        img_url = _url[:-1] + i['src']
                        break
            except KeyError:
                print(f"\033[91m[ERROR]\033[0m couldnt find image at {_url}")
                continue

            req = re.get(img_url, timeout=5)
            if req.status_code != HTTP_SUCCESS:
                print(f"\033[91m[ERROR]\033[0m timeout at {img_url}")
                continue
             
            print(f"(https){img_url[8:30]} ==> {img_file_name}")
            with open(img_file_name, "wb") as img_file:
                for chunk in req.iter_content(chunk_size=50000):
                    img_file.write(chunk)

            img_count += 1

if __name__ == '__main__':
    try:
        os.mkdir('data')
    except FileExistsError:
        pass

    if(os.path.exists(html)): print("\033[94m[STATUS]\033[0m download_html is already done")
    else: download_html(school_list_url, html)
    if(os.path.exists(school_list_file)): print("\033[94m[STATUS]\033[0m parse_html_for_links is already done")
    else: parse_html_for_links(html, school_list_file)
    download_images_from_links(school_list_file, images)

