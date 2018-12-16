import os
import io
import re
import argparse
import requests
import zipfile

from urllib.parse import urlencode, urlparse, parse_qs
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
CONSOLES_DESCRIPTION_MAP = {
    'Super Nintendo': 'snes',
    'Nintendo':'nes',
    'Gameboy Advance': 'gba',
    'Gameboy Color': 'gbc',
    'Gameboy': 'gb',
    'Sega Genesis': 'genesis',
}
CONFIRMATION_INPUT = ['y', 'Y', 'n', 'N', 'yes', 'Yes', 'No', 'no']


def build_url(args, query, page):
    '''
    Build request url
    '''
    url = 'https://romsmania.cc/roms/'
    if args.console:
        url += CONSOLES_URL_MAP[args.console]+'/search'
    else:
        url += 'search/table'
    params = {'name': query, 'orderAsc':0, 'page': page, 'order':'downloads'}
    url += '?'+urlencode(params)
    print(url)
    return url


def get_rom_list(url, args):
    '''
    Parse page, get rom list and build dict with needed data
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    romset = soup.select('table')[0].find_all('tr')[1:]
    if len(romset) == 0:
            return None
    roms = []
    roms.append({})
    current_page = parse_qs(urlparse(url).query)['page'][0]
    roms[0]['current_page'] = current_page
    paginator = soup.select('.pagination')
    if len(paginator) == 0:
        roms[0]['last_page'] = '1'
    else:
        if paginator[0].find_all('a')[-1].text.strip() == 'Next':
            lastpage = paginator[0].find_all('a')[-2].text.strip()
        else:
            lastpage = paginator[0].find_all('a')[-1].text.strip()
        roms[0]['last_page'] = lastpage
    for source in romset:
        subset = source.find_all('td')
        rom = {}
        rom['number'] = romset.index(source)+1
        rom['link'] = subset[0].a['href']
        rom['link'] = rom['link'][:20] + '/download' + rom['link'][20:]
        rom['name'] = subset[0].a.text
        if args.console:
            rom['rating'] = subset[1].text
            rom['downloads'] = subset[2].text
        else:
            rom['console'] = subset[1].text
            rom['rating'] = subset[2].text
            rom['downloads'] = subset[3].text
        roms.append(rom)
    return roms


def download_and_extract(link, args, rom):
    r = requests.get(link)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    if args.console:
        path = args.romsdir + '/' + args.console
    elif rom:
        path = args.romsdir + '/' + CONSOLES_DESCRIPTION_MAP[rom['console']]
    else:
        path = args.romsdir
    z.extractall(path)
    for f in z.namelist():
        print("Extracted: " + path + '/' + f)



def printinfo(romlist):
    '''
    Print ROM list for selection
    '''
    offset = max([len(rom['name']) for rom in romlist[1:]])+1
    if 'console' in romlist[1]:
        print('№  ' + 'Title'+' '*(offset-len('Title')) + 'Console' + 5*' ' +'Rating' + ' '*3 + 'Downloads')
        for rom in romlist[1:]:
            print(str(rom['number'])+ ' '*(3-len(str(rom['number']))) + rom['name']
                  + ' '*(offset-len(rom['name'])) + rom['console'] + 5*' ' +  rom['rating'] +' '*6 + rom['downloads'])
            print()
            print('-'*offset)
    else:
        print('№  ' + 'Title'+' '*(offset-len('Title')) +'Rating' + ' '*3 + 'Views')
        for rom in romlist[1:]:
            print(str(rom['number'])+ ' '*(3-len(str(rom['number']))) + rom['name']
                  + ' '*(offset-len(rom['name'])) + rom['rating'] +' '*6 +
                rom['downloads'])
            print()
            print('-'*offset)
    print('Page {} of {}'.format(romlist[0]['current_page'], romlist[0]['last_page']))


def get_download_link(romlink):
    r = requests.get(romlink)
    newsoup = BeautifulSoup(r.text, "html.parser")
    link = newsoup.select('.wait__link')[0]['href']
    return link


def main():
    parser = argparse.ArgumentParser(description='Retro consoles ROM Downloader')
    parser.add_argument('query', type=str, nargs='+', help='search query')
    parser.add_argument('--console', choices=CONSOLES, help='console')
    parser.add_argument('--romsdir', '-r', default='/home/{}/roms'.format(os.getenv('USER')), help='roms directory')
    args = parser.parse_args()
    for query in args.query:
        url = build_url(args, query, 1)
        romlist = get_rom_list(url, args)
        if romlist is None:
            if not args.console:
                print('Sorry, No ROMs Found with \'{}\' keyword :('.format(query))
            else:
                print('Sorry, No ROMs Found with \'{}\' keyword for {} :('.format(query, args.console))
            continue
        printinfo(romlist)
        if len(romlist) == 2:
            confirm = input('\n> Do you wanna download this rom? (y/n): ')
            while not confirm in CONFIRMATION_INPUT:
                confirm = input('\n> Please, enter y or n (y/n): ')
            if confirm in [choice for choice in CONFIRMATION_INPUT if choice.startswith('y') or choice.startswith('Y')]:
                link = get_download_link(romlist[1]['link'])
            else:
                continue
        else:
            page = input('\n> Please, select the ROM you need (just number), or enter page number as pN: ')

            while not (page in [str(rom['number']) for rom in romlist[1:]]) and not (re.match('p\d+$', page) and int(page.split('p')[1]) <= int(romlist[0]['last_page']) and int(page.split('p')[1]) >= 1):
                page = input('\n> Please, select the ROM you need (just number), or enter page number as pN: ')
            while re.match('p\d+$', page):
                page = page.split('p')[1]
                if int(page) <= int(romlist[0]['last_page']) and int(page) >= 1:
                    url = build_url(args, query, page)
                    romlist = get_rom_list(url, args)
                    if romlist is None:
                        if not args.console:
                            print('Sorry, No ROMs Found with \'{}\' keyword :('.format(query))
                        else:
                            print('Sorry, No ROMs Found with \'{}\' keyword for {} :('.format(query, args.console))
                        continue
                    printinfo(romlist)
                    if len(romlist) == 1:
                        confirm = input('\n> Do you wanna download this rom? (y/n): ')
                        while not confirm in CONFIRMATION_INPUT:
                            confirm = input('\n> Please, enter y or n (y/n): ')
                            link = get_download_link(romlist[1]['link'])
                    else:
                        page = input('\n> Please, select the ROM you need (just number), or enter page number as pN: ')
                        while not (page in [str(rom['number']) for rom in romlist[1:]]) and not (re.match('p\d+$', page) and int(page.split('p')[1]) <= int(romlist[0]['last_page']) and int(page.split('p')[1]) >= 1):
                            page = input('\n> Please, select the ROM you need (just number), or enter page number as pN: ')
            link = get_download_link(romlist[int(page)]['link'])
        download_and_extract(link, args, romlist[int(page)])


if __name__ == "__main__":
    main()
