import click
from click import echo as cprint, style as st
import inquirer
from inquirer.themes import GreenPassion
from models.player import *
from models.board import *


class Game:
    PLAYER1 = 'player1'
    PLAYER2 = 'player2'
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.__opponent = None
        self.turn = 0

    @property
    def opponent(self):
        return self.__opponent

    def get_opponent(self):
        q = [
            inquirer.List('choice', message='Play with', choices=['Computer', 'Friend'])
        ]
        answer = inquirer.prompt(q, theme=GreenPassion())
        self.__opponent = answer['choice']
        return Player.register(self.__opponent, Game.PLAYER2) if self.__opponent == 'Computer' else  self.get_player(Game.PLAYER2)
           
    def get_player(self, player_type):
        q = [
            inquirer.Text('name', message=f'What is {player_type} name', validate=lambda _, x: re.match('[a-zA-Z]', x))
        ]
        answer= inquirer.prompt(q)
        return Player.register(answer['name'], player_type)
    

    def play(self, player,opponent):    
        print('Your turn' if self.turn==0 else 'Player2 turn')                         
        if opponent.ship_count > 0: 
            if  self.__opponent == 'Computer' and player.type == Game.PLAYER2:      
                coords = opponent.random_coords()
            else:
                q = [
                        inquirer.Text('x', message=f"x  (column: [a-j/A-J])", validate=lambda _, x: re.match('^[a-jA-J]{1}$',  x)),
                        inquirer.Text('y', message=f"y  (row: [0-9])", validate=lambda _, x: re.match('^\d{1}$', x)),
                    ]
                coords = inquirer.prompt(q)
                coords['x'] = int(opponent.COLS[coords['x'].lower()])
            self.turn = 0 if self.turn == 1 else 1
            opponent.hit(**{
                'x': coords['x'],
                'y': int(coords['y']),
                'player': player
            })           
        else:
            raise NameError('Game Over')
        

    
