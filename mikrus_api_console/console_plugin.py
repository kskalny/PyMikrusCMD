from abc import ABC, abstractmethod,abstractproperty

class MikrusCMDPlugin(ABC):
    @abstractproperty
    def name(self):
        pass
    
    @abstractproperty
    def author(self):
        pass

    @abstractproperty
    def version(self):
        pass

    @abstractproperty
    def __doc__(self):
        pass
    
    @abstractproperty
    def commands(self):
        pass
    
    @abstractmethod
    def __init__(self, mikrus_console):
        pass
