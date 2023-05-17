import json


class parse:
    __parse = None

    def __init__(self,path : str) -> None:
        self.path = path

    def json(self) -> str:
        try:
            with open(self.path, 'r') as f:
                __data = json.load(f)
            return __data
        except Exception as __e:
            print(__e)
            return __e
    
    def yaml(self):
        pass

    def xml(self):
        pass
