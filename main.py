from models.ship import *
from typing import List
import click
from click import echo as cprint, style as st
import inquirer
from inquirer.themes import GreenPassion
from models.game import *
from models.print import *  

def initialize():
    '''
    user is asked about informations about player1, 
    and user has options to continue game with:
        computer or player,
    if computer is selected, coordinates of ships are determined randomly;
    if player is selected, player2 must enter infos about himself/herself and ships
    
    '''

    header()
    game = Game()
    game.player1 = game.get_player('player1')
    game.player2 = game.get_opponent()

    set_ships_text('player1', game.player1.name)
    game.player1.board.set_ships('player')

    set_ships_text('player2', game.player2.name)
    game.player2.board.set_ships(game.opponent)

    return game

if __name__ == '__main__':
    game = initialize()
    PLAY = '1: Play'
    MY_BOARD = '2: Print your board'
    OPPONENT_BOARD = '3: Print opponent board'
    STATISTICS = '4: Statisctics'
    
    EXIT = '5: Exit'
    RESTART = '6: Re-start'
    
    q = [
        inquirer.List('choice',
        message='Select',
        choices=[PLAY, MY_BOARD, OPPONENT_BOARD, STATISTICS, EXIT, RESTART])
    ]
    while True:
        try:
            answer = inquirer.prompt(q)
            player = game.player1 if game.turn == 0 else game.player2
            opponent = game.player2 if game.turn == 0 else game.player1
            if answer['choice'] == PLAY:   
                try:        
                    print_board(opponent.board)
                    game.play(player, opponent.board)
                except ValueError as err:
                    print(err)
                except NameError as err:
                    raise NameError(err)                  
                finally:
                     if game.opponent == 'Computer' and game.turn == 1:
                        game.play(opponent, player.board)
            elif answer['choice'] == MY_BOARD:
                print(f'\tPlayer1: {player.name}\tShoots: {player.shoots}\tPoints: {player.points}')
                print_board(player.board)
            elif answer['choice'] == OPPONENT_BOARD:
                print(f'\tPlayer2: {opponent.name}\tShoots: {opponent.shoots}\tPoints: {opponent.points}')
                print_opponent_board(opponent)
            elif answer['choice'] == STATISTICS:
                print_statistics(player)
            elif answer['choice'] == EXIT:
                print(exit_game(game.player1, game.player2))
                break
            elif answer['choice'] == RESTART:                
                initialize()
        except NameError:
            print(exit_game(game.player1, game.player2))
            result = continue_or_leave()
            if result == 'Yes':
                initialize()
            else:       
                print('Good Bye!')        
                break
        except Exception as err:
            print(err)

    


