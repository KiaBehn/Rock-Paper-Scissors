import pygame
import math
import random
import time
from pygame import mixer

pygame.init()


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


Game_Continue = False
Game_running = True
running = True
Game_Draws = 0
draw_time = 0
round_pause = False
count = 0
anim_reverse = False
game_eval_flag = False
Winner = ""
Pause_flag = False
Player1_Option = ""
Player2_Option = ""
Player1_Stats = Stats()
Player1_Stats.Name = "YOU"
Player2_Stats = Stats()
Player2_Stats.Name = "CPU"

# Screen and Background
screen = pygame.display.set_mode((1280, 720))
background = pygame.image.load('Pictures/rock paper scissors background.png')

# Background Music
bar_ambience = mixer.Sound("Sounds & Music/Bar Cocktail.mp3")
bar_ambience.play(-1)
# running = True
Card_Move_Sound = mixer.Sound("Sounds & Music/Card move.mp3")
Card_Play_Sound = mixer.Sound("Sounds & Music/Card play.mp3")

Options = ["Rock", "Paper", "Scissor"]
values = {'Rock': "Scissor", 'Paper': "Rock", 'Scissor': "Paper"}
Card_Index = 0
Card_Played = -1

Card_Rock = pygame.image.load('Pictures/Rock Card.png')
Card_Rock_Select = pygame.image.load('Pictures/Rock Card selected.png')
RockX = 360
RockY = 460

Card_Paper = pygame.image.load('Pictures/Paper Card.png')
Card_Paper_Select = pygame.image.load('Pictures/Paper Card selected.png')
PaperX = 560
PaperY = 460

Card_Scissors = pygame.image.load('Pictures/Scissors Card.png')
Card_Scissors_Select = pygame.image.load('Pictures/Scissors Card selected.png')
ScissorsX = 760
ScissorsY = 460

Scroll_animation4 = pygame.image.load('Pictures/scrolls 4.png')
Scroll_animation3 = pygame.image.load('Pictures/scrolls 3.png')
Scroll_animation2 = pygame.image.load('Pictures/scrolls 2.png')
Scroll_animation1 = pygame.image.load('Pictures/scrolls 1.png')
Scroll_animation = [Scroll_animation1, Scroll_animation2, Scroll_animation3, Scroll_animation4]

# Font
font_big_big = pygame.font.Font('Fonts/alagard.ttf', 64)
font_big = pygame.font.Font('Fonts/alagard.ttf', 34)
move_txtX = 560
move_txtY = 100
font = pygame.font.Font('Fonts/alagard.ttf', 26)
font_medium = pygame.font.Font('Fonts/alagard.ttf', 30)

# Title and Icon of the game
pygame.display.set_caption("Pixie RPS")
icon = pygame.image.load('Pictures/rock-paper-scissors small.png')
pygame.display.set_icon(icon)


def draw_scroll():
    scroll_pos_x = 450
    scroll_pos_y = 50
    screen.blit(Scroll_animation[count], (scroll_pos_x, scroll_pos_y))


def draw_moves(name, option):
    draw_pos_x = 510
    draw_pos_y = 150
    player_move_txt = font_big.render(name + " played " + option, True, (0, 0, 0))
    screen.blit(player_move_txt, (draw_pos_x, draw_pos_y))


def draw_winner(player):
    draw_pos_x = 510
    draw_pos_y = 150
    if player == "Draw":
        player_move_txt = font_big.render(player, True, (0, 0, 0))
    else:
        player_move_txt = font_big.render(player + " Won", True, (0, 0, 0))
    screen.blit(player_move_txt, (draw_pos_x, draw_pos_y))


def draw_cards():
    if Card_Played != 0:
        if Card_Index == 0:
            screen.blit(Card_Rock_Select, (RockX, RockY - 30))
        else:
            screen.blit(Card_Rock, (RockX, RockY))
    if Card_Played != 1:
        if Card_Index == 1:
            screen.blit(Card_Paper_Select, (PaperX, PaperY - 30))
        else:
            screen.blit(Card_Paper, (PaperX, PaperY))
    if Card_Played != 2:
        if Card_Index == 2:
            screen.blit(Card_Scissors_Select, (ScissorsX, ScissorsY - 30))
        else:
            screen.blit(Card_Scissors, (ScissorsX, ScissorsY))


def scroll_anim(func_receive):
    pause_round, drawtime, counter, animation_rev, option, name_pl, winner, move_draw_flag = func_receive
    pause_flag = False
    if drawtime != 0 and not animation_rev:
        pause_round = True
        drawtime -= 1
        if counter < 3 and drawtime % 10 == 0:
            counter += 1

        draw_scroll()
        if drawtime < 80:
            draw_moves(name_pl, option) if not move_draw_flag else draw_winner(winner)

        if drawtime == 1:
            animation_rev = True
            drawtime = 50

    elif drawtime != 0 and animation_rev:
        pause_round = True
        draw_scroll()
        if drawtime <= 40:
            if counter > 0 and drawtime % 10 == 0:
                counter -= 1
        else:
            draw_moves(name_pl, option) if not move_draw_flag else draw_winner(winner)
        drawtime -= 1
        if drawtime == 0:
            animation_rev = False
            pause_round = False
            pause_flag = True
            counter = 0
            drawtime = 120
    return pause_round, drawtime, counter, animation_rev, pause_flag


def game_eval(game_draws):
    if Player2_Option in values[Player1_Option]:
        Player1_Stats.win()
        Player2_Stats.loose()
        winner = "YOU"
    elif Player1_Option in values[Player2_Option]:
        Player2_Stats.win()
        Player1_Stats.loose()
        winner = "CPU"
    else:
        game_draws += 1
        winner = "Draw"
    return game_draws, winner


def draw_stats():
    stats_x = 75
    stats_y = 195
    player2_name_show = font_medium.render("(CPU Stats) ", True, (46, 173, 214))
    screen.blit(player2_name_show, (stats_x + 5, stats_y))
    wins = font.render("CPU WINS: " + str(Player2_Stats.Times_Won), True, (27, 109, 209))
    screen.blit(wins, (stats_x, stats_y + 35))
    streak = font.render("CPU Streak: " + str(Player2_Stats.Streak), True, (27, 109, 209))
    screen.blit(streak, (stats_x - 2, stats_y + 65))
    points = font.render("CPU Points: " + str(Player2_Stats.Points), True, (27, 109, 209))
    screen.blit(points, (stats_x - 2, stats_y + 95))

    player1_name_show = font_medium.render("(Player Stats)", True, (160, 109, 24))
    screen.blit(player1_name_show, (stats_x - 6, stats_y + 170))
    wins = font.render("PL. WINS: " + str(Player1_Stats.Times_Won), True, (170, 162, 39))
    screen.blit(wins, (stats_x, stats_y + 205))
    streak = font.render("PL. Streak: " + str(Player1_Stats.Streak), True, (170, 162, 39))
    screen.blit(streak, (stats_x, stats_y + 235))
    streak = font.render("PL. Points: " + str(Player1_Stats.Points), True, (170, 162, 39))
    screen.blit(streak, (stats_x, stats_y + 265))

    streak = font_medium.render("Draws: " + str(Game_Draws), True, (112, 112, 112))
    screen.blit(streak, (stats_x + 20, stats_y + 320))


def winner_eval():
    winner_list = ["", ""]
    if Player1_Stats.Streak == 3 or Player2_Stats.Streak == 3:
        winner_list[1] = "having a streak of 3 wins"
        winner_list[0] = Player1_Stats.Name if Player1_Stats.Streak == 3 else Player2_Stats.Name
    else:
        winner_list[1] = "points difference"
        winner_list[0] = Player1_Stats.Name if Player1_Stats.Points > Player2_Stats.Points else Player2_Stats.Name

    return winner_list


def game_over(winner, win_cause):
    pos_x = 365
    pos_y = 300
    game_over_screen = pygame.image.load('Pictures/Gameover screen.png')
    screen.blit(game_over_screen, (0, 0))
    sentence = winner + " Won due to " + win_cause
    text = font.render(sentence, True, (100, 0, 0))
    screen.blit(text, (pos_x, pos_y))

    sentence = "You had " + str(Player1_Stats.Times_Won) + " Wins          CPU had "
    sentence += str(Player2_Stats.Times_Won) + " Wins"
    text = font_medium.render(sentence, True, (0, 0, 0))
    screen.blit(text, (pos_x, pos_y + 40))

    sentence = "You had " + str(Player1_Stats.Points) + " Points        CPU had "
    sentence += str(Player2_Stats.Points) + " Points"
    text = font_medium.render(sentence, True, (0, 0, 0))
    screen.blit(text, (pos_x, pos_y + 80))

    sentence = "You had " + str(Player1_Stats.Streak) + " Streak       CPU had "
    sentence += str(Player2_Stats.Streak) + " Streak"
    text = font_medium.render(sentence, True, (0, 0, 0))
    screen.blit(text, (pos_x, pos_y + 120))

    sentence = "The game drew " + str(Game_Draws) + " times."
    text = font_medium.render(sentence, True, (0, 0, 0))
    screen.blit(text, (pos_x + 120, pos_y + 200))

    pygame.display.update()
    time.sleep(1)
    pygame.event.get()

    sentence = "Press the space bar"
    text = font.render(sentence, True, (150, 0, 0))
    screen.blit(text, (pos_x + 160, pos_y + 280))

    sentence = "if you want to start another game!"
    text = font.render(sentence, True, (150, 0, 0))
    screen.blit(text, (pos_x + 70, pos_y + 305))

    sentence = "OR press the ESCAPE button to QUIT!"
    text = font.render(sentence, True, (150, 50, 0))
    screen.blit(text, (pos_x + 68, pos_y + 335))

    game_over_running = True
    while game_over_running:
        for end_event in pygame.event.get():
            if end_event.type == pygame.QUIT:
                game_over_running = False
                exit()
            if end_event.type == pygame.KEYDOWN:
                if end_event.key == pygame.K_SPACE:
                    game_running = True
                    game_continue = True
                    return game_running, game_continue
                if end_event.key == pygame.K_ESCAPE:
                    exit()
        pygame.display.update()


# Game loop
while Game_running:
    player_difference = math.fabs(Player1_Stats.Points - Player2_Stats.Points)
    win_condition = Player1_Stats.Streak < 5 and Player2_Stats.Streak < 5 and player_difference < 50 and running

    while win_condition:

        screen.fill((50, 0, 0))
        screen.blit(background, (0, 0))
        if not round_pause:
            Info_X = 900
            Info_Y = 20
            Info = font.render("Press the space bar to play", True, (11, 186, 197))
            screen.blit(Info, (Info_X, Info_Y))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    win_condition = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if Card_Index != 0:
                            Card_Move_Sound.play()
                            Card_Index -= 1
                    if event.key == pygame.K_RIGHT:
                        if Card_Index != 2:
                            Card_Move_Sound.play()
                            Card_Index += 1
                    if event.key == pygame.K_SPACE:
                        Card_Play_Sound.play()
                        Player1_Option = Options[Card_Index]
                        Player2_Option = random.choice(Options)

                        # Evaluate the winner - loser - draws
                        Game_Draws, Winner = game_eval(Game_Draws)
                        draw_cards()
                        draw_time = 120
                        count = 0
                        Card_Played = -1
                        round_pause = True

        if not round_pause:
            draw_cards()
        draw_stats()
        if round_pause:
            winner_flag = False
            # Show your moves - currently disabled
            # if not Pause_flag and not game_eval_flag:
            #     Name = "You"
            #     Func_send = (round_pause, draw_time, count, anim_reverse, Player1_Option, Name, Winner, winner_flag)
            #     (round_pause, draw_time, count, anim_reverse, Pause_flag) = scroll_anim(Func_send)
            Pause_flag = True

            if Pause_flag and not game_eval_flag:
                Name = "CPU"
                Func_send = (round_pause, draw_time, count, anim_reverse, Player2_Option, Name, Winner, winner_flag)
                (round_pause, draw_time, count, anim_reverse, Pause_flag) = scroll_anim(Func_send)
                if not Pause_flag:
                    Pause_flag = True
                else:
                    Pause_flag = False
                    game_eval_flag = True
            if game_eval_flag:
                Name = ""
                winner_flag = True
                Func_send = (round_pause, draw_time, count, anim_reverse, Player2_Option, Name, Winner, winner_flag)
                (round_pause, draw_time, count, anim_reverse, Pause_flag) = scroll_anim(Func_send)
                if Pause_flag:
                    winner_flag = False
                    game_eval_flag = False
                    Pause_flag = False
                    round_pause = False

        pygame.display.update()
        # Faster game end for testing
        # while Player1_Stats.Points < 2 and running and Player2_Stats.Points < 2:
        # win_condition = Player1_Stats.Points < 2 and running and Player2_Stats.Points < 2

        # Full game rules
        player_difference = math.fabs(Player1_Stats.Points - Player2_Stats.Points)
        win_condition = Player1_Stats.Streak < 5 and Player2_Stats.Streak < 5 and player_difference < 50 and running

    winner_details = winner_eval()
    Game_running, Game_Continue = game_over(winner_details[0], winner_details[1])
    if Game_Continue:
        Game_running = True
        running = True
        Game_Draws = 0
        draw_time = 0
        round_pause = False
        count = 0
        anim_reverse = False
        game_eval_flag = False
        Winner = ""
        Pause_flag = False
        Player1_Option = ""
        Player2_Option = ""
        Player1_Stats.__init__()
        Player2_Stats.__init__()
        Player1_Stats.Name = "YOU"
        Player2_Stats.Name = "CPU"
        Game_Continue = False
