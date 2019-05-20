class Ship():
    def __init__(self, name, abbrev, count, length):
        self.__name = name
        self.__count = count
        self.__length = length
        self.__abbrev = abbrev
         
    @property
    def name(self):
        return self.__name

    @property 
    def count(self):
        return self.__count
        
    @property
    def abbrev(self):
        return self.__abbrev

    @property 
    def length(self):
        return self.__length

    @property 
    def abbrev(self):
        return self.__abbrev   
