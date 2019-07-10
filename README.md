# retrolover
Command-line simple ROM automatic downloader for your retropie

After downloading it automatically extracts zip archive to your roms folder

### source has been changed to the romsmania so that tool is working again

install:

`pip install retrolover`

Usage:

`~ retrolover --console snes Castlevania`


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
