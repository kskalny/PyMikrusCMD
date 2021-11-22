from termcolor import colored, cprint

def print_error(message:str):
    cprint(message, color='red', attrs=['bold'])

def print_info(message:str):
    cprint(message, color='blue')

def print_with_colors(messages:list):
    for message in messages:
        cprint(message[0], **message[1])