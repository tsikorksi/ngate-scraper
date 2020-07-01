# maybe remove?
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import os
import textwrap

base_url = "http://n-gate.com"


def download(url):
    """
    Downloads from n-gate, checks for network errors

    :return: the sitemap HTML
    """
    try:
        sitemap = urllib.request.urlopen(f'{base_url}{url}')
    except urllib.error.URLError:
        return None
    if sitemap.getcode() != 200:
        return None
    return sitemap.read()


def parse_links(html, string):
    """
    Finds all the links to pages in sitemap

    :param html: the html of the sitemap
    :param string: the searched for string, pointing to the type of post
    :return: the url of each post
    """
    output = []
    soup = BeautifulSoup(html, 'html.parser')
    for item in soup.find_all('li'):
        if string in item.string:
            output.append(item.find('a').get('href'))

    return output


def gets_urls(section, yearly=False):
    """
    Formats and cleans the urls

    :param section: the links for a particular site section
    :param yearly: whether or not dates are per year
    :return: the post links
    """
    posts = []
    for post in section:
        struct = post.split('/')
        if yearly:
            posts.append((struct[2], post))
        else:
            posts.append((struct[2:-2], post))
    return posts


def page_parser(url):
    """
    The text and data associated with a section of posts, placed into a dictionary

    :param url: the post url
    :return: the week of posts as a list, formatted
    """
    page = download(url)
    if page is None:
        return
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


def conference_parser(url):
    """
    Parses a FOSDEM conference page into readable sections

    :param url: the url of the conference post
    :return: the text data, list of section dicts
    """
    section = {
        "Title": "",
        "Text": []
    }
    temp = []

    page = download(url)
    page = BeautifulSoup(page, 'html.parser')
    page = page.find('div', {"id": "main-copy"})
    page = page.find_all(['p', 'h3'])

    text = page[0].text.split('\n')
    sections = [text[0]]
    text[0] = ''
    for i in range(0, len(text)):
        try:
            if text[i+1] == '' and text[i-1] == '':
                section["Text"] = temp[1:]
                sections.append(section)
                section = section.fromkeys(section, "")
                section["Title"] = text[i]
                temp = []
            else:
                temp.append(text[i])
        except IndexError:
            continue

    section["Text"] = temp[2:]
    sections.append(section)

    sections.pop(1)

    return sections


def print_post(week):
    """
    pretty-prints each post with a prompt

    :param week: a group of posts
    :return: if quit command was sent, then false
    """
    for day in week[1:]:
        cls(after=f'{week[0]}\n')
        print(f"\n\t{day['Title']}\n\t{(day['url'])}\n\t{day['Date']}\n")
        print('\n\t'.join(textwrap.wrap(f"\t{day['Text']}\n(n for next, q for quit)>")), end='')
        if get_next():
            print()
            continue
        else:
            return False


def conference_print(year):
    """
    pretty prints each year by section

    :param year: the text data for a conference year
    :return: False if quit
    """
    for section in year[1:]:
        cls(after=f'{year[0]}\n')
        print(f'\n{section["Title"]}\n')
        text = section["Text"]
        for i in range(0, len(text) - 1, 2):
            print(f'\t{text[i]}\n\n\t{text[i+1]}\n')
        print('\n(n for next, q for quit)>', end='\r')
        if get_next():
            continue
        else:
            return False


def webshit_reader(posts):
    """
    Parse and output webshit weekly
    :param posts: parsed list of posts
    :return: return when quit signal sent
    """
    dates = []
    temp = '/hackernews/'

    for i in range(0, 3):
        times = []
        for post in posts:
            # Check that date section is not already found and valid for the rest of the date
            if post[0][i] not in times and post[1].startswith(temp) is True:
                times.append(post[0][i])
        times.sort()
        choice = menu(times)
        if not choice:
            return
        time = times[choice - 1]
        dates.append(time)
        temp += time + '/'

    i = 0
    # get index of searched for post
    for i in range(0, len(posts)):
        if posts[i][0] == dates:
            break

    # parse from that point
    for post in posts[i:]:
        for week in page_parser(post[1]):
            if not print_post(week):
                return


def get_next():
    """
    Simple CLI prompt

    :return: true if next, false if quit
    """
    while True:
        n = input('\n')
        if n == 'n':
            return True
        elif n == 'q':
            return False


def cls(after=''):
    """
    Clears the screen, optionally adding an ending

    :param after: the optional ending string
    :return: Clears terminal
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print(after, end='')


def print_banner():
    """
    Prints a pretty banner

    :return: A banner
    """
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


def menu(options):
    """
    Menu generator

    :param options: the possible options
    :return: the chosen option, or False if exit
    """
    while True:
        print(f"[0] - Exit")
        for index, item in enumerate(options):
            print(f"[{index + 1}] - {item}")
        try:
            output = int(input(">"))
        except ValueError:
            continue
        if output < 0 or output > len(options):
            continue
        elif output == 0:
            return False
        else:
            return output


def main():
    """
    Main terminal parser
    TODO: argument mode, search

    :return:
    """
    options = ['Latest Post', 'FOSDEM: more boring shit', 'Webshit Weekly', 'About']

    print_banner()

    # Attempt Connection
    print("Querying Website...", end='')
    html = download('/sitemap')
    if html is None:
        print("\n Unable to connect to n-gate.com, please check connection!")
        exit(1)
    else:
        print("Done!\n")

    while True:

        section = menu(options)
        if section == 1:
            # Latest
            for week in page_parser(''):
                if not print_post(week):
                    break

        elif section == 2:
            # FOSDEM
            fosdem = parse_links(html, 'FOSDEM')
            posts = gets_urls(fosdem, True)

            choice = menu([post[0] for post in posts])
            conference_print(conference_parser(posts[choice - 1][1]))

        elif section == 3:
            # Webshit
            weekly = parse_links(html, 'webshit weekly')
            posts = gets_urls(weekly)
            webshit_reader(posts)

        elif section == 4:
            # About
            continue

        elif not section:
            exit(0)

        print_banner()


main()
