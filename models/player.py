from models.board import *

class Player:
    def __init__(self, name, player_type):
        self.name = name
        self.points = 0
        self.shoots = 0
        self.board = Board()
        self.type = player_type
    
    @classmethod 
    def register(cls, name, player_type):
        return cls(name, player_type)