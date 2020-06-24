# maybe remove?
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import os
import textwrap

base_url = "http://n-gate.com"


def download_map():
    try:
        sitemap = urllib.request.urlopen(f'{base_url}/sitemap')
    except urllib.error.URLError:
        return None
    if sitemap.getcode() != 200:
        return None
    return sitemap.read()


def parse_links(html, string):
    output = []
    soup = BeautifulSoup(html, 'html.parser')
    for item in soup.find_all('li'):
        if string in item.string:
            output.append(item.find('a').get('href'))

    return string


def gets_urls(section, yearly=False):
    posts = []
    for post in section:
        struct = post.split('/')
        if yearly:
            posts.append((struct[2], post))
        else:
            posts.append((struct[2:-2], post))
    return posts


def page_parser(url):
    page = urllib.request.urlopen(f'{base_url}{url}')
    page = BeautifulSoup(page, 'html.parser')
    posts = page.find_all('p')

    weeks = []
    week = []
    day = {
        "url": "",
        "Title": "",
        "Date": "",
        "Text": ""
    }
    for post in posts:
        text = post.get_text().split('\n')
        if text[0] == 'Navigation:':
            continue
        elif text[0].startswith('An annotated digest'):
            weeks.append(week)
            week = [text[0]]
        elif text[0] == '':
            day['url'] = post.find_next('a').get('href')
            day["Title"] = text[1]
            day["Date"] = text[2]
            day["Text"] = text[4]
            week.append(day)
            day = day.fromkeys(day, "")

    weeks.append(week)
    return weeks[1:]


def print_post(week):
    for day in week[1:]:
        cls(after=f'{week[0]}\n')
        print(f"\n\t{day['Title']}\n\t{(day['url'])}\n\t{day['Date']}\n")
        print('\n\t'.join(textwrap.wrap(f"\t{day['Text']}\n(n for next, q for quit)>")), end='')
        if get_next():
            print()
            continue
        else:
            return False


def get_next():
    while True:
        n = input('')
        if n == 'n':
            return True
        elif n == 'q':
            return False


def cls(after=''):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(after, end='')


def print_banner():
    cls()
    banner = """
    n-gate.com. we can't both be right. 
                                   
    MMMMMN0OOOOOOOOOOOOOOOOOOXMMMMMMMMMMMMMM
    MMMMMk;cdddddddddddddddddddkKWMMMMMMMMMM
    MMMMMx;OMMMMMMMMMMMMMMMMMNKOdxKWMMMMMMMM
    ddddd:,OMMMMMMMMMMMMMMMMMMMMNOdkXMMMMMMM
    ;;,;;.'OMMMMMMMMMMMMMMMMMMMMMMNxlOMMMMMM
    MWMWWx;OMMMMMMMMMMMMMMMMMMMMMMMNklOMMMMM
    MMMMMx;OMMMMMMMMMMMMMMMMMMMMMMMMK;,dk000
    MMMMMx;OMMMMMMMMMMMMMMMMMMMMMMMMK;:kc'''
    MMMMMx;OMMMMMMMMMMMMMMMMMMMMMMMMK;;dk00K
    MMMMMx;OMMMMMMMMMMMMMMMMMMMMMMMNklOMMMMM
    kkkkkc,OMMMMMMMMMMMMMMMMMMMMMMNxlOMMMMMM
    '''',.'OMMMMMMMMMMMMMMMMMMMMXkdkXMMMMMMM
    NNNNNx;OMMMMMMMMMMMMMMMMMN0OdkXMMMMMMMMM
    MMMMMO;cdddddddddddddddddddkXWMMMMMMMMMM
    MMMMMWK000000000000000000XWMMMMMMMMMMMMM      
    """
    print(banner)
    print("N-Gate reader created by Osirian\n")
    print("Please donate to the source: https://www.patreon.com/ngate\n")


def main():
    options = ['Latest Post', 'FOSDEM: more boring shit', 'Webshit Weekly', 'Software', 'About', 'Exit']

    print_banner()

    # Attempt Connection
    print("Querying Website...", end='')
    html = download_map()
    if html is None:
        print("\n Unable to connect to n-gate.com, please check connection!")
        exit(1)
    else:
        print("Done!\n")

    while True:

        for index, item in enumerate(options):
            print(f"[{index +1 }] - {item}")
        try:
            section = int(input(">"))
        except ValueError:
            section = 0
        if section == 1:
            # Latest
            for week in page_parser(''):
                if not print_post(week):
                    break

        elif section == 2:
            # FOSDEM
            fosdem = parse_links(html, 'FOSDEM')
            posts = gets_urls(fosdem, True)
            for post in posts:
                for week in page_parser(post):
                    print_post(week)

        elif section == 3:
            weekly = parse_links(html, 'webshit weekly')
            # Webshit
            for post in weekly:
                for week in page_parser(post):
                    print_post(week)
        elif section == 4:
            # Software
            continue
        elif section == 5:
            # About
            continue
        elif section == 6:
            exit(0)

        print_banner()


main()
