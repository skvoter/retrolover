import argparse
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup

CONSOLES = ['snes','nes','gba','gbc','gb','genesis']
CONSOLES_URL_MAP = {
    'snes': 'super-nintendo',
    'nes': 'nintendo',
    'gba': 'gameboy-advance',
    'gbc': 'gameboy-color',
    'gb': 'gameboy',
    'genesis': 'sega-genesis'
}


def build_url(args, term):
    '''
    Build request url
    '''
    url = 'https://www.loveroms.com/roms/'
    if args.console:
        url += CONSOLES_URL_MAP[args.console]+'/'
    params = {'q': term, 'page': 1, 'order':'downloads'}
    url += '?'+urlencode(params)
    return url


def get_rom_list(url):
    '''
    Parse page, get rom list and build dict with needed data
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    romset = soup.select('#view-full')[0].find_all('tr')[1:]
    if len(romset) == 1:
        if 'Sorry, No ROMs Found :(' in romset[0].text:
            return None

def main():
    parser = argparse.ArgumentParser(description='Retro consoles ROM Downloader')
    parser.add_argument('term', type=str, nargs='+', help='search term')
    parser.add_argument('--console', choices=CONSOLES, help='console')
    args = parser.parse_args()
    for term in args.term:
        url = build_url(args, term)
        romlist = get_rom_list(url)
        if romlist is None:
            if not args.console:
                print('Sorry, No ROMs Found with \'{}\' keyword :('.format(term))
            else:
                print('Sorry, No ROMs Found with \'{}\' keyword for {} :('.format(term, args.console))

main()
