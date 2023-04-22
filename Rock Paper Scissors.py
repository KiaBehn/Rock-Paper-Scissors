import random
import math
import time

Options = ["Rock", "Paper", "Scissor"]
Game_Draws = 0
values = {'Rock': "Scissor", 'Paper': "Rock", 'Scissor': "Paper"}


class Stats:
    def __init__(self):
        self.Times_Won = 0
        self.Times_Lost = 0
        self.Points = 0
        self.Streak = 0
        self.Name = "Player"

    def win(self):
        self.Times_Won += 1
        self.Points += 2 ** self.Streak
        self.Streak += 1

    def loose(self):
        self.Times_Lost += 1
        self.Streak = 0


class GameSettings:
    Players_Num = 1
    Player1_Randomizer = 0
    Player2_Randomizer = 1


GameSet = GameSettings()
Player1_Stats = Stats()
Player1_Stats.Name = "Player 1"
Player2_Stats = Stats()
Player2_Stats.Name = "Computer"

Game_Continue = True


def game_settings():
    while True:
        option = input(f'''
        SETTINGS:
        
        1. Change the number of players: {GameSet.Players_Num}
        2. Randomizer for {Player1_Stats.Name}:  {GameSet.Player1_Randomizer}
        {f"3. Randomizer for Player2: {GameSet.Player2_Randomizer}" if GameSet.Players_Num == 2 else
        "   Player2 is The Computer"} 
        4. Return
        ''')

        if int(option) == 1:
            GameSet.Player2_Randomizer = 1
            if GameSet.Players_Num == 1:
                GameSet.Players_Num = 2
                Player2_Stats.Name = "Player 2"
                print("Changed the number of players from 1 to 2 you will control player 2 ...")
            else:
                GameSet.Players_Num = 1
                Player2_Stats.Name = "The Computer"
                print("Changed the number of players from 2 to 1 Computer will control player 2...")
        elif int(option) == 2:
            print("Player 1 Choices will be randomized...") if GameSet.Player1_Randomizer == 0 else print(
                "Player 1 Choices will no longer be randomized...")
            GameSet.Player1_Randomizer = 0 if GameSet.Player1_Randomizer == 1 else 1
        elif int(option) == 3:
            if GameSet.Players_Num == 2:
                print("Player 2 Choices will be randomized...") if GameSet.Player2_Randomizer == 0 else print(
                    "Player 2 Choices will no longer be randomized...")
                GameSet.Player2_Randomizer = 0 if GameSet.Player2_Randomizer == 1 else 1
        else:
            print("Returning to main menu...")
            break
    return


def initial_game():
    while True:
        option = input(f'''
 (Rock Paper Scissor The Game)
1. Start
2. Settings
3. Exit
    ''')
        if int(option) == 1:
            break
        elif int(option) == 2:
            game_settings()
        else:
            exit()


def game_eval(game_draws):
    if Player2_Option in values[Player1_Option]:
        Player1_Stats.win()
        Player2_Stats.loose()
        print(f"{Player1_Stats.Name} won this round")
    elif Player1_Option in values[Player2_Option]:
        Player2_Stats.win()
        Player1_Stats.loose()
        print(f"{Player2_Stats.Name} won this round")
    else:
        print("This round was a draw")
        game_draws += 1
    return game_draws


def game_details_draw():
    print(f'''
{Player1_Stats.Name} chose '{Player1_Option}' and {Player2_Stats.Name} chose '{Player2_Option}'
    {Player1_Stats.Name} Stats:
    {Player1_Stats.Name} Wins:          {Player1_Stats.Times_Won}
    {Player1_Stats.Name} Points:        {Player1_Stats.Points}
    {Player1_Stats.Name} Streak:        {Player1_Stats.Streak}

    {Player2_Stats.Name} Stats:
    {Player2_Stats.Name} Wins:          {Player2_Stats.Times_Won}
    {Player2_Stats.Name} Points:        {Player2_Stats.Points}
    {Player2_Stats.Name} Streak:        {Player2_Stats.Streak}
    ''')


def game_over(winner, win_cause):
    print(f'''      GAME OVER
{winner} Won due to {win_cause}
    
{Player1_Stats.Name} had {Player1_Stats.Points} points
{Player1_Stats.Name} won {Player1_Stats.Times_Won} rounds and lost {Player1_Stats.Times_Lost} 

{Player2_Stats.Name} had {Player2_Stats.Points} points
{Player2_Stats.Name} won {Player2_Stats.Times_Won} rounds and lost {Player2_Stats.Times_Lost} 

and the game drew {Game_Draws} rounds

''')

    time.sleep(2)
    option_flag = True
    while option_flag:
        option = input("Press 1 to start another game or press 0 to exit: \n")
        if option == "1":
            name1 = Player1_Stats.Name
            name2 = Player2_Stats.Name
            Player1_Stats.__init__()
            Player2_Stats.__init__()
            Player1_Stats.Name = name1
            Player2_Stats.Name = name2
            option_flag = False
        elif option == "0":
            exit()


def winner_eval():
    winner_list = ["", ""]
    if Player1_Stats.Streak == 5 or Player2_Stats.Streak == 5:
        winner_list[1] = "having a streak of 5 wins"
        winner_list[0] = Player1_Stats.Name if Player1_Stats.Streak == 5 else Player2_Stats.Name
    else:
        winner_list[1] = "points difference"
        winner_list[0] = Player1_Stats.Name if Player1_Stats.Points > Player2_Stats.Points else Player2_Stats.Name

    return winner_list


initial_game()
while Game_Continue:
    while Player1_Stats.Streak < 5 and Player2_Stats.Streak < 5 and math.fabs(
            Player1_Stats.Points - Player2_Stats.Points) < 50:
        if GameSet.Player1_Randomizer == 1:
            Player1_Option = random.choice(Options)
        else:
            Player1_Option = ""
            while Player1_Option not in ['1', '2', '3']:
                print("Player1 : \n")
                Player1_Option = input("1.Rock , 2.Paper , 3.Scissor:\n")
            Player1_Option = Options[int(Player1_Option) - 1]

        if GameSet.Player2_Randomizer == 1:
            Player2_Option = random.choice(Options)
        else:
            Player2_Option = ""
            while Player2_Option not in ['1', '2', '3']:
                print("Player2 : \n")
                Player2_Option = input("1.Rock , 2.Paper , 3.Scissor:\n")
            Player2_Option = Options[int(Player2_Option) - 1]

        Game_Draws = game_eval(Game_Draws)
        game_details_draw()

        input("Press any button...")

    winner_details = winner_eval()
    game_over(winner_details[0], winner_details[1])
