"""

Author: Guy Shuster

Purpose: A custom P2P client implementing the Submarines game

Date: 29/12/2020

Usage: python main.py

"""

import game_manager


def main():
    print('\nStarting the Submarines game')
    print('*********************************************************************************************************\n')
    game_manager.GameManager().main_game_loop()
    print('\n*********************************************************************************************************')
    print('Game finished! Thanks for playing...')


if __name__ == '__main__':
    main()
