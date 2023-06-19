class Player:
    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        self.__name = name
