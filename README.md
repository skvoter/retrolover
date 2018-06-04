# retrolover
Command-line simple Loveroms.com ROM automatic downloader

install:

`git clone https://github.com/skvoter/retrolover`

`pipenv install`

Usage:
```
python retrolover.py --help                                                   
usage: retrolover.py [-h] [--console {snes,nes,gba,gbc,gb,genesis}]
                     [--romsdir ROMSDIR]
                     query [query ...]

Retro consoles ROM Downloader

positional arguments:
  query                 search query

optional arguments:
  -h, --help            show this help message and exit
  --console {snes,nes,gba,gbc,gb,genesis}
                        console
  --romsdir ROMSDIR, -r ROMSDIR
                        roms directory
```

TODO:
- add to pip
- make setup.py script
- make it independent package
- add more consoles
