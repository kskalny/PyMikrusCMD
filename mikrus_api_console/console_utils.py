from termcolor import colored, cprint

def print_error(message:str):
    cprint(message, color='red', attrs=['bold'])

def print_info(message:str):
    cprint(message, color='blue')

def print_exec_response(message:str, exit_code:int=0):
    if exit_code:
        cprint(message, color='red')
    else:
        cprint(message, color='green')

def print_with_colors(messages:list):
    for message in messages:
        cprint(message[0], **message[1])