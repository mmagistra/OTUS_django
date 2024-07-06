from time import sleep

import requests
import bs4


def find_hrefs(url, exists_links=None, remaining_depth=-1):
    if exists_links is None:
        exists_links = []

    remaining_depth -= 1
    if remaining_depth != 0:
        sleep(1)
        try:
            response = requests.get(url, headers)
        except requests.exceptions.RequestException as e:
            return 'Bad url'

        soup = bs4.BeautifulSoup(response.text, "lxml")
        response.close()

        # links = [link.get('href') for link in soup.find_all('a') if link not in exists_links]
        links = list()
        for link in soup.find_all('a'):
            link = link.get('href')
            if (link is not None
                    and link not in ('', '/', '#')
                    and not any(map(lambda x: link.startswith(x), BAN_LINKS))):
                if not (link.startswith('http:') or link.startswith('https:')):
                    if link[0] == '/':
                        link = main_url+link
                    else:
                        link = main_url+'/'+link
                if link not in exists_links:
                    links.append(link)
                    exists_links.append(link)

        if len(links) == 0:
            return 'No new links found'
        # Use if u need find path to link
        next_links = {link: find_hrefs(link, exists_links, remaining_depth) for link in links}
        return exists_links
    else:
        return 'Depth limitation'


def find_sites():
    # inputs
    print('''This program check all links on selected site.
The program looks for links to new sites and displays all unique cases.''')
    url = input('Enter the url with which the program will work: ')
    depth = int(input('The program uses recursion, enter its available depth: '))
    out = input('Where print results? Console or output file (C/F)? ')

    # check input
    if out == 'C' or out == 'F':
        print('Input is received')
    else:
        print(f'Please type C or F, u typed: {out}')
        return

    # code
    links = find_hrefs(url, remaining_depth=depth)
    unique_links = [url]
    for link in links:
        if not any(map(lambda x: link.startswith(x), unique_links)):
            unique_links.append("/".join(link.split('/')[:3]))

    if out == 'C':
        unique_links = "\n".join(unique_links)
        print(f'Unique sites:\n{unique_links}')
    elif out == 'F':
        with open('output.txt', 'w') as f:
            unique_links = "\n".join(unique_links)
            f.write(f'Unique sites:\n{unique_links}')
        print('File output.txt contains the results.')


# settings
BAN_LINKS = (
    'https://twitter.com',
)

st_accept = "text/html"
st_useragent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15")
headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}
main_url = 'https://tumen.biskvitdvor.ru'
depth = 2

# code
find_sites()
