import random

#=======================================================

def choose_options():
    Options = ('Rock', 'Paper', 'Scissors')
    Player_1 = input('Player 1: rock, paper or scissors? ')
    Player_1 = Player_1.capitalize()
    Player_2 = random.choice(Options)

    if Player_1 not in Options:
        print('That option is not valid!')
    #continue
        return None, None

    print('Player 1 chose: ',Player_1)
    print('Player 2 chose: ',Player_2)
    return Player_1, Player_2

#=======================================================

def game_rules(Player_1, Player_2, UserScore, ComputerScore):
    if Player_1 == Player_2:
        print('Draw!')
    elif Player_1 == 'Rock': 
        if Player_2 == 'Scissors':
            print('Player 1 wins, rock beats scissors!')
            UserScore += 1
        else:
            print('Player 1 lost, paper beats rock!')
            ComputerScore += 1
    elif Player_1 == 'Paper':
        if Player_2 == 'Rock':
            print('Player 1 wins, paper beats rock!')
            UserScore += 1
        else:
            print('Player 1 lost, Scissors beats paper!')
            ComputerScore += 1
    elif Player_1 == 'Scissors':
        if Player_2 == 'Paper':
            print('Player 1 wins, scissors beats paper!')
            UserScore += 1
        else:
            print('Player 1 lost, rock beats scissors!')
            ComputerScore += 1
    return UserScore, ComputerScore
    
#=======================================================

def run_game():

    UserScore = 0
    ComputerScore = 0

    Rounds = 1

    while True:
        print('*' * 10)
        print('Round', Rounds)
        print('*' * 10)

        Rounds += 1

        Player_1, Player_2 = choose_options()
        UserScore, ComputerScore = game_rules(Player_1, Player_2, UserScore, ComputerScore)

        print('User Score:', UserScore)
        print('Computer Score:', ComputerScore)

        if ComputerScore == 3:
            print('The computer won!')
            break

        if UserScore == 3:
            print('You won!')
            break

#=======================================================

run_game()
