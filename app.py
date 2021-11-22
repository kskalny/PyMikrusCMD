from typing import DefaultDict
from mikrus_api_console.console import MikrusCMD
from mikrus_api_console.console_utils import print_error
from getpass import getpass
from os import environ
from sys import exit

if __name__=="__main__":
    MIKRUS_API = environ.get('MIKRUS_API') or getpass('Podaj klucz API:\t')
    MIKRUS_SRV = environ.get('MIKRUS_SRV') or input('Podaj numer serwera:\t')
    LANGUAGE = environ.get('LANG')
    if MIKRUS_API is None or MIKRUS_SRV is None:
        print_error('Ustaw zmienne środowiskowe <MIKRUS_API> i <MIKRUS_SRV> by skożystać z narzędzia.')
        exit(1)
    MikrusCMD(
        api_key=MIKRUS_API,
        srv=MIKRUS_SRV
    ).cmdloop()