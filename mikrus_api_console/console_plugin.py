from abc import ABC,abstractproperty


def MikrusCMDPlugin(ABC):
    @abstractproperty
    def name(self):
        pass
    
    @abstractproperty
    def author(self):
        pass

    @abstractproperty
    def version(self):
        pass
    
