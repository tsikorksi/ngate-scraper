# maybe remove?
from bs4 import BeautifulSoup
import urllib.request

base_url = "http://n-gate.com"

def download_map():
    sitemap = urllib.request.urlopen(f'{base_url}/sitemap')
    if (sitemap.getcode() != 200):
        return None
    return sitemap.read()

def parse_links(html):
    fosdem = []
    weekly = []
    soup = BeautifulSoup(html, 'html.parser')
    for item in soup.find_all('li'):
        if ('webshit weekly' in item.string):
            weekly.append(item.find('a').get('href'))
        elif ('FOSDEM' in item.string):
            fosdem.append(item.find('a').get('href'))
    return fosdem, weekly

def choose_date(section, yearly=False):
    posts = []
    for post in section:
        struct = post.split('/')
        if (yearly):
            posts.append((struct[2], post))
        else:
            posts.append((struct[2:-2], post))
    return posts


def main(section=2):
    banner = """                               
                            _                               
    _ __         __ _  __ _| |_ ___   ___ ___  _ __ ___     
    | '_ \ _____ / _` |/ _` | __/ _ \ / __/ _ \| '_ ` _ \    
    | | | |_____| (_| | (_| | ||  __/| (_| (_) | | | | | |_  
    |_| |_|      \__, |\__,_|\__\___(_)___\___/|_| |_| |_(_) 
                |___/                                       
                                    _ _     _           _   _       _                 _       _     _     
    __      _____    ___ __ _ _ __ ( ) |_  | |__   ___ | |_| |__   | |__   ___   _ __(_) __ _| |__ | |_   
    \ \ /\ / / _ \  / __/ _` | '_ \|/| __| | '_ \ / _ \| __| '_ \  | '_ \ / _ \ | '__| |/ _` | '_ \| __|  
    \ V  V /  __/ | (_| (_| | | | | | |_  | |_) | (_) | |_| | | | | |_) |  __/ | |  | | (_| | | | | |_ _ 
    \_/\_/ \___|  \___\__,_|_| |_|  \__| |_.__/ \___/ \__|_| |_| |_.__/ \___| |_|  |_|\__, |_| |_|\__(_)
                                                                                        |___/             
    """
    print(banner)
    print("Parser created by Osirian\n")
    print("Please donate to the source: https://www.patreon.com/ngate")
    html = download_map()
    if (html == None):
        print("Unable to connect to n-gate.com, please check connection...")
        exit(1)
    else:
        fosdem, weekly = parse_links(html)
        if (section == 1):
            posts = choose_date(fosdem, True)
        elif (section == 2):
            posts = choose_date(weekly)
        

main()