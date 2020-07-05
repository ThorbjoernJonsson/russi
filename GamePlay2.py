from network import Network
import pygame
pygame.font.init()
import time


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
grey = (192, 192, 192)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)
deal = {'w': 120, 'h': 60, 'x':30, 'y':30}
leave = {'w': 120, 'h': 60, 'x':30, 'y':550}
btns = [Button("Deal", deal['x'], deal['y'], (0, 250, 0), deal['w'], deal['h']),
        Button("Quit", leave['x'], leave['y'], (255, 0, 0), leave['w'], leave['h'])]
Color_line = (255, 0, 0)
y_place_line = int((deal['y'] + leave['y'])/2 + 22)
font = pygame.font.Font('freesansbold.ttf', 18)
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

    pygame.draw.line(win, Color_line, (deal['x'], y_place_line), (deal['x'] + 1200, y_place_line), 4)
    text0_new = font.render('Score ' + str(score[0]), True, blue, grey)
    text1_new = font.render('Score ' + str(score[1]), True, blue, grey)
    win.blit(text0_new, textRect0)
    win.blit(text1_new, textRect1)
    for i in range(len(deck)):
        if deck[i][2] == 1:
            img = pygame.image.load("cards_gif/b1fv.gif")
            win.blit(img, deck[i][1])
        elif deck[i][2] == 0:
            img = pygame.image.load("cards_gif/" + deck[i][0] + ".gif")
            win.blit(img, deck[i][1])
    pygame.display.update()

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

    pygame.draw.line(win, Color_line, (deal['x'], y_place_line), (deal['x']+1200, y_place_line), 4)

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

        if game.redraw:
            if player == 0:
                win = redrawWindow(win, game.deck_p1, game.score)
            else:
                win = redrawWindow(win, game.deck_p2, game.score)
        if game.moves[0] != False and game.moves[1] != False:
            if player == 0:
                n.send('score')

        if game.num_cards_left == 0:
            if game.score[0] > game.core[1]:
                if player == 0:
                    text_in_middle('You Win!')
                else:
                    text_in_middle('You Lose!')
            elif game.score[0] < game.core[1]:
                if player == 0:
                    text_in_middle('You Lose!')
                else:
                    text_in_middle('You Win!')
            else:
                text_in_middle('It is a draw!')
            time.sleep(2)
            win = redrawWindow(win, game.deck_p1, game.score)



        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for i in range(len(game.deck_p1)):
                    if pos[0] >= game.deck_p1[i][1][0] and pos[0] <= game.deck_p1[i][1][0] + 70 and pos[1] >= game.deck_p1[i][1][1] and \
                        pos[1] <= game.deck_p1[i][1][1] + 95:
                        player_1_allowed = True
                        player_2_allowed = True
                        if player == 0:
                            if game.deck_p1[i][2] == 0 and (i <= 7 or (i >= 16 and i <= 33)):
                                player_1_sort = game.deck_p1[i][0][0]
                                if game.moves[1]:
                                    player_2_sort = game.moves[1][0]
                                    if player_1_sort != player_2_sort and game.num_sorts_p1[num_for_sort[player_2_sort]] > 0:
                                        player_1_allowed = False
                                        text_in_middle('You have ' + name_of_sorts[player_2_sort] + '!')
                                        time.sleep(2)
                                        win = redrawWindow(win, game.deck_p1, game.score)

                                if player_1_allowed:
                                    if i == 17 or i == 19 or i == 21 or i == 23 or i == 25 or i == 27 or i == 29 or \
                                        i == 31 or i == 33:
                                        n.send("flip," + str(i-1))
                                    n.send(str(i) + "," + str(1000) + "," + str(y_place_line - 110))
                                    if (not game.moves[0]) and (not game.moves[1]):
                                        n.send("first")
                        else:
                            if game.deck_p2[i][2] == 0 and ((i >= 8 and i <= 15) or i >= 34):
                                player_2_sort = game.deck_p2[i][0][0]
                                if game.moves[0]:
                                    player_1_sort = game.moves[0][0]
                                    if player_1_sort != player_2_sort and game.num_sorts_p2[num_for_sort[player_1_sort]] > 0:
                                        player_2_allowed = False
                                        text_in_middle('You have ' + name_of_sorts[player_1_sort] + '!')
                                        time.sleep(2)
                                        win = redrawWindow(win, game.deck_p2, game.score)

                                if player_2_allowed:
                                    if i == 35 or i == 37 or i == 39 or i == 41 or i == 43 or i == 45 or i == 47 or \
                                        i == 49 or i == 51:
                                        n.send("flip," + str(i-1))
                                    n.send(str(i) + "," + str(1000) + "," + str(y_place_line + 30))
                                    if (not game.moves[0]) and (not game.moves[1]):
                                        n.send("first")

                if btns[0].click(pos):
                    n.send("draw")


                elif btns[1].click(pos):
                    run = False
                    pygame.quit()

if __name__ == "__main__":
    main()
