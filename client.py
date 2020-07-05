# File name: client.py
# Runs the game russi.
# Created by Thorbjoern Jonsson

from network import Network
import pygame
import time
pygame.font.init()

#Define the Buttons and when clicked make sure it returns True
class Button:
    def __init__(self, text, x, y, color, w, h):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = w
        self.height = h

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 20)
        text = font.render(self.text, 1, (70, 10 , 50))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


width = 1250
height = 625

#Define the colors used
grey = (192, 192, 192)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)
deal = {'w': 120, 'h': 60, 'x':30, 'y':30}
leave = {'w': 120, 'h': 60, 'x':30, 'y':550}
btns = [Button("Deal", deal['x'], deal['y'], (0, 250, 0), deal['w'], deal['h']),
        Button("Quit", leave['x'], leave['y'], (255, 0, 0), leave['w'], leave['h'])]
y_place_line = int((deal['y'] + leave['y'])/2 + 22)
font = pygame.font.Font('freesansbold.ttf', 18)

#Define the text for the score for player 0 and player 1, it starts at 0
text0 = font.render('Score 0', True, blue, grey)
text1 = font.render('Score 0', True, blue, grey)
textRect0 = text0.get_rect()
textRect1 = text1.get_rect()
textRect0.center = (deal['x']+40, y_place_line - 30)
textRect1.center = (deal['x'] + 40, y_place_line + 30)
num_for_sort = {'h': 0, 's': 1, 'd': 2, 'c': 3}
name_of_sorts = {'h': 'hearts', 's': 'spades', 'd': 'diamonds', 'c': 'clubs'}

def redrawWindow(win, deck, score):
    win = pygame.display.set_mode((width, height))
    win.fill(grey)
    for btn in btns:
        btn.draw(win)

    pygame.draw.line(win, red, (deal['x'], y_place_line), (deal['x'] + 1200, y_place_line), 4)
    text0_new = font.render('Score ' + str(score[0]), True, blue, grey)
    text1_new = font.render('Score ' + str(score[1]), True, blue, grey)
    win.blit(text0_new, textRect0)
    win.blit(text1_new, textRect1)

    #Plot the card. If 1 then it points down, if it points up it is 0.
    for i in range(len(deck)):
        if deck[i][2] == 1:
            img = pygame.image.load("cards_gif/b1fv.gif")
            win.blit(img, deck[i][1])
        elif deck[i][2] == 0:
            img = pygame.image.load("cards_gif/" + deck[i][0] + ".gif")
            win.blit(img, deck[i][1])
    pygame.display.update()

#Deletes everything from the screen and returns a text in the middle on the interface
def text_in_middle(text_to_display):
    win = pygame.display.set_mode((width, height))
    win.fill(grey)
    font = pygame.font.Font('freesansbold.ttf', 60)
    text_have_sort = font.render(text_to_display, True, red, grey)
    textRect_have_sort = text_have_sort.get_rect()
    textRect_have_sort.center = (deal['x'] + 400, y_place_line)
    win.blit(text_have_sort, textRect_have_sort)
    pygame.display.update()


def main():
    win = pygame.display.set_mode((width, height))
    win.fill(grey)

    pygame.display.set_caption("Russi")

    for btn in btns:
        btn.draw(win)

    pygame.draw.line(win, red, (deal['x'], y_place_line), (deal['x']+1200, y_place_line), 4)

    win.blit(text0, textRect0)
    win.blit(text1, textRect1)
    pygame.display.update()

    run = True
    clock = pygame.time.Clock()
    n = Network()
    p1 = n.getP()
    player = int(n.getP())
    print ('You are player', player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        #Keep redrawing the interface so if there are change in location of cards or scores, it gets updated
        if game.redraw:
            if player == 0:
                win = redrawWindow(win, game.deck_p0, game.score)
            else:
                win = redrawWindow(win, game.deck_p1, game.score)
        if game.moves[0] != False and game.moves[1] != False:
            if player == 0:
                n.send('score')

        #Tells you if you won or lost, game.show_results is True and False to make sure you only show the winning/losing
        #once
        if game.num_cards_left == 0 and game.show_results :
            n.send("finished")
            if game.score[0] > game.score[1]:
                if player == 0:
                    text_in_middle('You Win!')
                else:
                    text_in_middle('You Lose!')
            elif game.score[0] < game.score[1]:
                if player == 0:
                    text_in_middle('You Lose!')
                else:
                    text_in_middle('You Win!')
            else:
                text_in_middle('It is a draw!')
            time.sleep(2)
            win = redrawWindow(win, game.deck_p0, game.score)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                #Go through every single card to check which one player 0 and player 1 pushed.
                for i in range(len(game.deck_p0)):
                    if pos[0] >= game.deck_p0[i][1][0] and pos[0] <= game.deck_p0[i][1][0] + 70 and pos[1] >= game.deck_p0[i][1][1] and \
                        pos[1] <= game.deck_p0[i][1][1] + 95:
                        player_0_allowed = True
                        player_1_allowed = True
                        if player == 0:

                            #Make sure player 0 is pushing his cards
                            if game.deck_p0[i][2] == 0 and (i <= 7 or (i >= 16 and i <= 33)):
                                player_0_sort = game.deck_p0[i][0][0]

                                #Check if there is a card out there by player 1 and if so make sure that if you have
                                #same sort that you play that sort. It gives you a warning if you try another sort.
                                if game.moves[1]:
                                    player_1_sort = game.moves[1][0]
                                    if player_0_sort != player_1_sort and game.num_sorts_p0[num_for_sort[player_1_sort]] > 0:
                                        player_0_allowed = False
                                        text_in_middle('You have ' + name_of_sorts[player_1_sort] + '!')
                                        time.sleep(2)
                                        win = redrawWindow(win, game.deck_p0, game.score)

                                #Update who's turn it is. This only happens in the beginning to find out who starts.
                                if game.next_play_player == -1:
                                    n.send("next_play_player, 0")

                                #If it is player 1 turn, player 0 get's told it's not his turn.
                                if game.next_play_player == 1:
                                    text_in_middle('It is not your turn')
                                    time.sleep(2)
                                    win = redrawWindow(win, game.deck_p0, game.score)

                                #If player 0 is allowed to play, couple of things happen. 1) First you check if player
                                #pushed a card that is on top of a card that is pointing down. If so it will get flipped
                                #in the next round. 2) Send which card is getting pushed and where it will be located.
                                #3) Update who's turn it is, now it is player 1's turn. 4) If there is no card out there
                                #then player 0 becomes first. It is done so that if player 0 and 1 have different sort
                                #then the player that is first wins that round.
                                if player_0_allowed and game.next_play_player == 0:
                                    if i == 17 or i == 19 or i == 21 or i == 23 or i == 25 or i == 27 or i == 29 or \
                                        i == 31 or i == 33:
                                        n.send("flip," + str(i-1))
                                    n.send(str(i) + "," + str(1000) + "," + str(y_place_line - 110))
                                    n.send("next_play_player, 1")
                                    if (not game.moves[0]) and (not game.moves[1]):
                                        n.send("first")
                        else:
                            #See comments for player 0. Everyhting reversed between player 0 and player 1
                            if game.deck_p1[i][2] == 0 and ((i >= 8 and i <= 15) or i >= 34):
                                player_1_sort = game.deck_p1[i][0][0]
                                if game.moves[0]:
                                    player_0_sort = game.moves[0][0]
                                    if player_0_sort != player_1_sort and game.num_sorts_p1[num_for_sort[player_0_sort]] > 0:
                                        player_1_allowed = False
                                        text_in_middle('You have ' + name_of_sorts[player_0_sort] + '!')
                                        time.sleep(2)
                                        win = redrawWindow(win, game.deck_p1, game.score)

                                if game.next_play_player == -1:
                                    n.send("next_play_player, 1")

                                if game.next_play_player == 0:
                                    text_in_middle('It is not your turn')
                                    time.sleep(2)
                                    win = redrawWindow(win, game.deck_p1, game.score)

                                if player_1_allowed and game.next_play_player == 1:
                                    if i == 35 or i == 37 or i == 39 or i == 41 or i == 43 or i == 45 or i == 47 or \
                                        i == 49 or i == 51:
                                        n.send("flip," + str(i-1))
                                    n.send(str(i) + "," + str(1000) + "," + str(y_place_line + 30))
                                    n.send("next_play_player, 0")
                                    if (not game.moves[0]) and (not game.moves[1]):
                                        n.send("first")

                if btns[0].click(pos):
                    n.send("draw")

                elif btns[1].click(pos):
                    run = False
                    pygame.quit()

if __name__ == "__main__":
    main()
