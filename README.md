# retrolover
Command-line simple Loveroms.com ROM automatic downloader

install:

`pip install retrolover`

Usage:
```
retrolover --help                                                   
usage: retrolover [-h] [--console {snes,nes,gba,gbc,gb,genesis}]
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
- add more consoles
- add ddos cloudflare check bypass
