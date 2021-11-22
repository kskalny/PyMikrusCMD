from cmd import Cmd
from os import error
from typing import List
from requests import post
from sys import exit
from mikrus_api_console.console_plugin import MikrusCMDPlugin
from mikrus_api_console.console_utils import print_error, print_exec_response, print_info, print_with_colors
from pprint import pprint

class ApiException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

API_URL = 'https://api.mikr.us/'

ENDPOINTS = [
    (path.strip(), description.strip()) for (path, description) in (map(lambda x: x.split('-'), """\
/info       - informacje o Twoim serwerze (cache=60s)
/serwery    - listuje wszystkie Twoje serwery (cache=60s)
/restart    - restartuje Twój serwer 
/logs       - podgląd ostatnich logów [10 sztuk]
/amfetamina - uruchamia amfetaminę na serwerze (zwiększenie parametrów)
/db         - zwraca dane dostępowe do baz danych (cache=60s);
/stats      - statystyki użycia dysku, pamięci, uptime itp. (cache=60s)
/porty      - zwraca przypisane do Twojego serwera porty TCP/UDP (cache=60s)\
""".splitlines()))
]
#Commands to patch
"""
/exec       - wywołuje polecenie/polecenia wysłane w zmiennej 'cmd' (POST) 
"""

def api_call(mikrus, endpoint):
    def inner(func):
        def wrapper(*args, **kwargs):
            if not isinstance(mikrus, MikrusCMD):
                print_error("Coś się popsuło i nie było mnie słychać.")
                exit(1)
            response = mikrus.api_action(endpoint)
            return func(*args, **kwargs, response=response)
        return wrapper
    return inner

def get_json(*args, response=None):
    return response.json()

def print_json(*args, response=None):
    if response is None:
        print_error("Coś się popsuło i nie było mnie słychać.")
    pprint(response.json())

def print_raw(*args, response=None):
    if response is None:
        print_error("Coś się popsuło i nie było mnie słychać.")
    print(response.text)



class MikrusCMD(Cmd):
    __api_key:str
    __srv:str
    __plugins:List[MikrusCMDPlugin] = []

    @property
    def prompt(self):
        return f'{self.__srv}> '

    def api_action(self, endpoint, additional_data={}):
        response = post(
                f'{API_URL}/{endpoint}',
                headers={
                    'UserAgent':'MikrusCMD',

                },
                data={
                    'key':self.__api_key,
                    'srv':self.__srv,
                    **additional_data
                }
            )
        if response.status_code == 403:
            raise ApiException(response.text)
        return response

    def __load_plugins(self, plugins):
        for plugin in plugins:
            self.__plugins.append(plugin(self))  

    def __init_plugins(self):
        for plugin in self.__plugins:
            for command in plugin.commands:
                plugin_command_name = plugin.name.replace(' ','_').lower()
                setattr(self, f'do_{plugin_command_name}_{command.__name__}',command) 


    def __init__(self, api_key:str, srv:str, plugins:List[MikrusCMDPlugin]=None) -> None:
        self.__api_key = api_key
        self.__srv = srv
        for (path, description) in ENDPOINTS:
            get_command = f'get_{path[1:]}_json'
            setattr(self, get_command, api_call(self, path)(get_json))
            command =  f'do_{path[1:]}'
            setattr(self, command, api_call(self, path)(print_json))
            getattr(self, command).__doc__ = '[JSON]' + description.title()
            command_raw = command + '_raw'
            setattr(self, command_raw, api_call(self, path+".raw")(print_raw))
            getattr(self, command_raw).__doc__ = '[RAW]' + description.title()

     

        self.__load_plugins(plugins)
        self.__init_plugins()
        print("Witaj administratorze!")
        try:
            self.do_expires()
        except ApiException as e:
            print_error(e)
            exit(1)

        super().__init__()

    


    def do_use(self, input:str=None, response=None):
        def change_name(servers):
            for server in response.json():
                if server['server_id'] == __server_name or server['server_name'] == __server_name:
                    self.__srv = server['server_id'] 
                    return True
            return False
            
        __server_name = input.strip()
        if __server_name=='':
            print_error('Musisz podać nazwę serwera do wyboru!')
            print(response.json())
        else:
            if change_name(self.get_serwery_json()):
                print_info(f'Zmieniles swoj wybor na serwer {self.__srv}')
            else:
                print_error('Serwer o takiej nazwie nie należy do Ciebie!')


    
    def do_expires(self,input:str=''):
        """
        Wyświetla dane wygaśnięcia usług na aktualnym serwerze.
        """
        data = self.get_info_json()
        print_with_colors([
            (f"""\
------------------
Daty wygaśnięcia usług dla {data['server_id']}:
------------------"""
                ,{'color':'blue'}
            ),
            (f'''\
VPS:\t\t{data['expires']}
CYTRUS:\t\t{data['expires_cytrus']}
STORAGE:\t{data['expires_storage']}
''',{}
            )]
        )

    def do_exec(self, input:str='', response=None):
        response = self.api_action('/exec', additional_data={
            'cmd':input.strip()+';echo $?;'
        })
        
        output_lines = response.json().get('output').replace('\\n','\n').splitlines()
        if output_lines:
            exit_code = int(output_lines[-1])

            print_exec_response("\n".join(output_lines[:-1]), exit_code)
        else:
            print_error("Coś poszło nie tak i nie było mnie słychać!")

    def do_shell(self, input:str=''):
        """
        Alias fo exec
        """
        self.do_exec(input)

    def do_exit(self, input:str='',):
        '''
        Exit the application
        '''
        return True

    def get_names(self):
        return dir(self)