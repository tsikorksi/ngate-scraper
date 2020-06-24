# maybe remove?
from bs4 import BeautifulSoup
import urllib.request
import urllib.error

base_url = "http://n-gate.com"


def download_map():
    try:
        sitemap = urllib.request.urlopen(f'{base_url}/sitemap')
    except urllib.error.URLError:
        return None
    if sitemap.getcode() != 200:
        return None
    return sitemap.read()


def parse_links(html):
    fosdem = []
    weekly = []
    soup = BeautifulSoup(html, 'html.parser')
    for item in soup.find_all('li'):
        if 'webshit weekly' in item.string:
            weekly.append(item.find('a').get('href'))
        elif 'FOSDEM' in item.string:
            fosdem.append(item.find('a').get('href'))
    return fosdem, weekly


def choose_date(section, yearly=False):
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
    post = BeautifulSoup(page, 'html.parser')
    posts = post.find_all('p')
    print(posts)

    # print(f"Post for {date[0]}/{date[1]}/{date[2]}")


def main():
    banner = """                               
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
    print("Reader created by Osirian\n")
    print("Please donate to the source: https://www.patreon.com/ngate")
    html = download_map()
    if html is None:
        print("\n Unable to connect to n-gate.com, please check connection...")
        exit(1)

    fosdem, weekly = parse_links(html)

    options = ['Latest Post', 'FOSDEM: more boring shit', 'Webshit Weekly', 'Software', 'About']
    chosen = False

    while not chosen:
        for index, item in enumerate(options):
            print(f"[{index +1 }] - {item}")
        section = int(input(">"))
        if section == 1:
            page_parser('')
            chosen = True
        elif section == 2:
            posts = choose_date(fosdem, True)
            chosen = True
        elif section == 3:
            posts = choose_date(weekly)
            chosen = True
        elif section == 4:
            chosen = True
        elif section == 5:

            chosen = True


main()
