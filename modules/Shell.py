from requests.api import get
from mikrus_api_console.console_plugin import MikrusCMDPlugin
from cmd import Cmd

def executeCommand(command):
    def wrapper(func):
        def inner(input, *args, **kwargs):
            return func(f"{command} {input}",*args,**kwargs)
        return inner
    return wrapper

class ShellCmd(Cmd):
    @property
    def prompt(self):
        return self.__mikrus_api.prompt+"(shell)# "

    def __init__(self, mikrus_api, *args, **kwargs):
        self.__mikrus_api = mikrus_api
        super().__init__()
        self.load_commands()
    

    def get_commands(self):
        response = self.__mikrus_api.api_action('/exec',{
            'cmd':"echo $PATH | tr ':' '\n' | xargs -n 1 ls -1"
        })
        return( response.json().get('output').split('\n'))

    def load_commands(self):
        for command in self.get_commands():
            self.__setattr__(f'do_{command}', executeCommand(command)(self.__mikrus_api.do_exec) )

    def do_exit(self, input:str=''):
        return True

    def get_names(self):
        return dir(self)


class ShellModule():
    """
    Sample Shell module 
    """
    @property
    def author(self):
        return 'Plugin Author'

    @property
    def version(self):
        return (0,0,1)

    @property
    def name(self):
        return 'Server Shell'

    def __init__(self, mikrus_console) -> None:
        self.__mikrus = mikrus_console
        # super().__init__()
        print('Initialized', self.name)

    @property
    def commands(self):
        return [
            self.shell
        ]

    def shell(self, input:str=''):
        ShellCmd(self.__mikrus).cmdloop()
    