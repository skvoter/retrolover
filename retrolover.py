#!/usr/bin/python3
import argparse
from bs4


def parseAndCollect():
    pass


def main():
    parser = argparse.ArgumentParser(description='Retro consoles ROM Downloader')
    parser.add_argument('term', type=str, help='search term')
    parser.add_argument('--console', help='console')
    args = parser.parse_args()

main()
