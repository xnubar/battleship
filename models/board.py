from models.ship import *
from typing import List
import inquirer
from inquirer.themes import GreenPassion
import re
from string import ascii_lowercase
from models.print import *
from random import randint, choice


class Board:
    COL_NUM = 10
    ROW_NUM = 10
    COLS = {letter: str(index) for index, letter in enumerate(ascii_lowercase, start=0)} 
    SHIP_TYPES = [
             Ship('Battleship', 'BT', 4, 1),
             Ship('Cruiser', 'CR', 3, 2),
             Ship('Destroyer', 'DT', 2, 3),
             Ship('Submarine', 'SB', 1, 4)
        ]
    BARRIER_SIGN = ' .'
    DEFAULT_SHIP_SIGN = '  '
    HIT_SHIP = ' X'
    WRONG_GUESS = ' O'

    def __init__(self):
        self.ships = []
        self.coordinates = self.initialize_board()
        self.__ship_count = 20

    @property
    def ship_count(self):
        return self.__ship_count

    def decr_ship_count(self):
        if self.__ship_count - 1 >= 0:
            self.__ship_count -= 1
    
        
    def initialize_board(self):
        return [[Board.DEFAULT_SHIP_SIGN for col in range(Board.COL_NUM)] for row in range(Board.ROW_NUM)]  

    def _set_barries_of_ship(self, ship, x, y):
        for x in range(Board.ROW_NUM):
            for y in range(Board.COL_NUM):
                if(self.coordinates[x][y]==ship.abbrev):
                    if x - 1 >= 0 and y - 1 >= 0 and self.coordinates[x - 1][y - 1] == Board.DEFAULT_SHIP_SIGN:
                        self.coordinates[x - 1][y - 1] = Board.BARRIER_SIGN
                    if y - 1 >= 0 and self.coordinates[x][y - 1] == Board.DEFAULT_SHIP_SIGN:
                        self.coordinates[x][y - 1] = Board.BARRIER_SIGN
                    if x + 1 < Board.COL_NUM and y - 1 >= 0 and self.coordinates[x + 1][y - 1] == Board.DEFAULT_SHIP_SIGN:
                        self.coordinates[x + 1][y - 1] = Board.BARRIER_SIGN
                    if x + 1 < Board.COL_NUM and self.coordinates[x + 1][y] == Board.DEFAULT_SHIP_SIGN:
                        self.coordinates[x + 1][y] = Board.BARRIER_SIGN
                    if x + 1 < Board.COL_NUM and  y + 1 < Board.ROW_NUM and self.coordinates[x + 1][y + 1] == Board.DEFAULT_SHIP_SIGN:
                        self.coordinates[x + 1][y + 1] = Board.BARRIER_SIGN
                    if y + 1 < Board.COL_NUM and self.coordinates[x][y + 1] == Board.DEFAULT_SHIP_SIGN:
                        self.coordinates[x][y + 1] = Board.BARRIER_SIGN
                    if x - 1 >= 0 and y + 1 < Board.ROW_NUM and self.coordinates[x - 1][y + 1] == Board.DEFAULT_SHIP_SIGN:
                        self.coordinates[x - 1][y + 1] = Board.BARRIER_SIGN
                    if x - 1 >= 0 and self.coordinates[x - 1][y] == Board.DEFAULT_SHIP_SIGN:
                        self.coordinates[x - 1][y] = Board.BARRIER_SIGN


    def add_ship(self, ship, x, y, direction):
        DIRECTION = 'horizontal'
        ship_position = x if DIRECTION else y
        ship_end = ship_position + ship.length
        result = self.ship_position_validation(ship_position, ship_end, x, y, direction)
        if result:
            for i in range(ship.length):            
                coordinate = y, x+i
                if direction == 'vertical':
                    coordinate = i+y, x
                self.coordinates[coordinate[0]][coordinate[1]] = ship.abbrev
            self._set_barries_of_ship(ship, *coordinate)
   
    def ship_position_validation(self, ship_position, ship_end, x, y, direction):
        for i in range(ship_end-ship_position):
            coordinate = y, x+i
            if direction == 'vertical':
                coordinate = i+y, x
            if not self.is_valid_coordinate(*coordinate):
                raise ValueError('Invalid coordinate!')
        return True
                         

    def is_valid_coordinate(self, x, y):
        return x in range(0,Board.ROW_NUM) and y in range(0, Board.ROW_NUM) and self.coordinates[x][y] == Board.DEFAULT_SHIP_SIGN


    def get_inputs(self, ship):
        q = [
        inquirer.Text('x', message=f"{ship.name} - x  (column: [a-j/A-J])", validate=lambda _, x: re.match('^[a-jA-J]{1}$', x)),
        inquirer.Text('y', message=f"{ship.name} - y  (row: [0-9])", validate=lambda _, x: re.match('^\d{1}$', x)),
        inquirer.List('direction', message='Direction', choices=['horizontal', 'vertical'])
    ]
        coords = inquirer.prompt(q, theme=GreenPassion())
        return {
            'x': int(Board.COLS[coords['x'].lower()]),
            'y': int(coords['y']),
            'direction': coords['direction']
        }
    
    def random_coords(self):
        return {
            'x': randint(0,9),
            'y': randint(0,9),
            'direction': choice([  'horizontal',
                                   'vertical']) 
        }

    def hit(self, x, y, player):
        if not x in range(0, 10)  or not y in range(0,10):
            raise ValueError('Invalid coordinates!')
        if  self.coordinates[y][x] == self.HIT_SHIP or self.coordinates[y][x]==self.WRONG_GUESS:
            raise ValueError('Invalid coordinates!')
        if self.coordinates[y][x] == self.DEFAULT_SHIP_SIGN  or self.coordinates[y][x]==self.BARRIER_SIGN:  
            self.coordinates[y][x] = self.WRONG_GUESS
            raise ValueError('Wrong guess...')
        else:
            self.coordinates[y][x] = self.HIT_SHIP
            player.points += 1
            self.decr_ship_count()



    def set_ships(self, player):      
        for ship in Board.SHIP_TYPES:
            length = ship.count
            while length>0:
                try:
                    if player == 'Computer':
                        coords = self.random_coords()
                    else:
                        print_board(self)
                        coords = self.get_inputs(ship)
                    self.add_ship(ship, **coords)
                    length -= 1
                except ValueError as err:
                    if player != 'Computer':
                        print(err)
