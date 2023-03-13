import requests as requests
from bs4 import BeautifulSoup

global links
links = 0
global file_num
file_num = 1
page = "https://briefly.ru"
headers = {"User-Agent": "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion"}
links_set = set()


def parse_v2(html_page, links, file_num):
    try:
        response = requests.get(html_page, headers=headers)
        response_headers = response.headers
    except Exception:
        return
    if "text/html" in response_headers["Content-Type"]:
        print(links)
        content = response.text
        with open(f"files/{file_num}.html", "w") as file:
            file.write(content)
            file_num += 1
        soup = BeautifulSoup(content, 'html.parser')
        links_from_html = set(soup.find_all('a', href=True))
        if len(links_set) <20:
            links_set.update(links_from_html)
            for link in links_from_html:
                if link.get('href') not in links_set:
                    links += 1
                    links_set.add(link.get('href'))
                    parsed_link = f"{page}{link.get('href')}"
                    parse_v2(parsed_link, links, file_num)


parse_v2(page, links, file_num)
