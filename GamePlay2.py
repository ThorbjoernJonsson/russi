
from graphics import *
import time
import random
from Deck import*
import time
from network import Network
import pygame
import pickle
pygame.font.init()


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
deal = {'w': 120, 'h': 60, 'x':30, 'y':30}
leave = {'w': 120, 'h': 60, 'x':30, 'y':550}
btns = [Button("Deal", deal['x'], deal['y'], (0, 250, 0), deal['w'], deal['h']),
        Button("Quit", leave['x'], leave['y'], (255, 0, 0), leave['w'], leave['h']),
        Button("Submit 1", 30, 110, (0, 255, 0), 120, 60), Button("Submit 2", 30, 470, (0, 255, 0), 120, 60)]
Color_line = (255, 0, 0)
y_place_line = int((deal['y'] + leave['y'])/2 + 22)
font = pygame.font.Font('freesansbold.ttf', 18)
text0 = font.render('Player 0', True, blue, grey)
text1 = font.render('Player 1', True, blue, grey)
textRect0 = text0.get_rect()
textRect1 = text1.get_rect()
textRect0.center = (deal['x']+40, y_place_line - 30)
textRect1.center = (deal['x'] + 40, y_place_line + 30)

def redrawWindow(win, game, p):
    return 1


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

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()


                if pos[0] >= game.deck_p1[0][1][0] and pos[0] <= game.deck_p1[0][1][0] + 70 and pos[1] >= game.deck_p1[0][1][1] and \
                    pos[1] <= game.deck_p1[0][1][1] + 95:
                    img = pygame.image.load("cards_gif/" + game.deck_p1[0][0] + ".gif")
                    win.blit(img, (1000, y_place_line - 110))
                    pygame.display.update()
                    game.deck_p1[0][1] = (1000, y_place_line - 110)
                    game.deck_p2[0][1] = (1000, y_place_line - 110)
                    game.deck_p2[0][2] = False
                    n.send(str(game.deck_p1[0][1][0]) + ','+ str(game.deck_p1[0][1][1]))
                    #n.send(game.deck_p1)
                    #data_string = pickle.dumps(str(game.deck_p1[0][1][0]) + ','+ str(game.deck_p1[0][1][1]))
                    #print (data_string)
                    #n.send(data_string)





                if btns[0].click(pos):
                    if player == 0:
                        for i in range(52):
                            if game.deck_p1[i][2]:
                                img = pygame.image.load("cards_gif/b1fv.gif")
                            else:
                                img = pygame.image.load("cards_gif/" + game.deck_p1[i][0] + ".gif")
                            #img = pygame.transform.scale(img, (80, 80))
                            win.blit(img, game.deck_p1[i][1])
                    else:
                        for i in range(52):
                            if game.deck_p2[i][2]:
                                img = pygame.image.load("cards_gif/b1fv.gif")
                            else:
                                img = pygame.image.load("cards_gif/" + game.deck_p2[i][0] + ".gif")
                            win.blit(img, game.deck_p2[i][1])
                    pygame.display.update()
                elif btns[1].click(pos):
                    run = False
                    pygame.quit()
                elif btns[2].click(pos) and game.connected():
                        n.send('player 0')
                elif btns[3].click(pos) and game.connected():
                    print ('reupdate')
                    for i in range(52):
                        if game.deck_p2[i][2]:
                            img = pygame.image.load("cards_gif/b1fv.gif")
                        else:
                            img = pygame.image.load("cards_gif/" + game.deck_p2[i][0] + ".gif")
                        win.blit(img, game.deck_p2[i][1])
                    pygame.display.update()
    #time.sleep(15)

if __name__ == "__main__":
    main()
