import click
from click import echo as cprint, style as st
from models.board import *

COLORS = {
    'BT': 'green',
    'CR': 'bright_yellow',
    'DT': 'magenta',
    'SB': 'cyan',
    '  ' :'white',
    ' .': 'blue',
    ' X': 'red',
    ' O': 'white',
    'header': 'cyan',
    'set_ships': 'yellow'
}


def header():
    print(st('\n\n\t\t\t*****************************************************************', fg=COLORS['header']))
    print(st('\t\t\t*\t\t\t  BATTLESHIP\t\t\t\t*\t', fg=COLORS['header']))
    print(st('\t\t\t*****************************************************************\n\n', fg=COLORS['header']))


def set_ships_text(player_num, player_name):
    print(st(f'> {player_num}: {player_name}, Set your ships to star game:\n', fg = COLORS['set_ships']))


def print_board(board):
    print('   _______________________________________________________________________________')
    print('  |     A       B       C       D       E       F       G       H       I       J |')
    print('  |_______________________________________________________________________________|')

    for r in range(board.ROW_NUM):
            print(f'\n|{r}|    ', end='')
            for c in range(board.COL_NUM):
                color = COLORS[board.coordinates[r][c]]
                print(st(board.coordinates[r][c], fg=color), end='      ')
            print()
    print('  |_______________________________________________________________________________')
    


def print_statistics(player):
    '''
    method prints information about player (name, points, shoots), also ships of player
    '''
    table_length = 80
    dash = '-' * table_length
    tab = '\t'
    print(dash)

    print(f'\tPlayer1: {player.name}', end=tab) 
    print(f'Points: {player.points}', end=tab)
    print(f'Shoots: {player.shoots}')
    print(dash)
    ship_counts = []
    for i in range(4):
        count = 0
        for r in range(player.board.ROW_NUM):
            for c in range(player.board.COL_NUM):
                if player.board.SHIP_TYPES[i].abbrev == player.board.coordinates[r][c]:
                    count += 1
        ship_counts.append(count)
    print('Ship\t\t Abbrev. \t\t Sunk')
    print(dash)
    for i in range(len(player.board.SHIP_TYPES)):
        print(f'{player.board.SHIP_TYPES[i].name} ', end='\t ')
        print(f'{player.board.SHIP_TYPES[i].abbrev} ', end='\t ')
        result = 'yes' if ship_counts[i]==0 else 'no'
        print(f'\t\t {result}')


def continue_or_leave():
    q = [
                inquirer.List('choice',
                              message="Do you want to continue",
                              choices=['Yes', 'No']),
            ]

    answer = inquirer.prompt(q,theme= GreenPassion())
    return answer['choice']

def exit_game(player1, player2):
    '''
    method returns string which contains results of players

    '''

    print(f'{player1.type}: {player1.name} \t | \t points: {player1.points}')
    print(f'{player2.type}: {player2.name} \t | \t points: {player2.points}')
    if player1.points > player2.points:
        return f'{player1.type} won ' 
    elif player2.points>player1.points:
        return f'{player2.type} won ' 
    else:
        return 'It\'s DRAW, GAME OVER...' 




def print_opponent_board(player):
    '''
    method prints game board of opponent, all ship types are hidden rather than destroyed, or wrong guessed ships 
    '''

    print('   _______________________________________________________________________________')
    print('  |     A       B       C       D       E       F       G       H       I       J |')
    print('  |_______________________________________________________________________________|')

    for r in range(player.board.ROW_NUM):
        print(f'\n|{r}|    ', end='')
        for c in range(player.board.COL_NUM):
            if player.board.coordinates[r][c] == player.board.HIT_SHIP or player.board.coordinates[r][c] == player.board.WRONG_GUESS:
                print(st(player.board.coordinates[r][c], fg=COLORS[player.board.coordinates[r][c]]), end='      ')
            else:
                print(st(player.board.BARRIER_SIGN, fg=COLORS[player.board.BARRIER_SIGN]), end='      ')