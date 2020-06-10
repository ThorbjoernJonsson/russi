
from graphics import *
import time
import random
from Deck import*
from Button import*
from Texts import*
import time
from network import Network
import pygame
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

class Game():
    def __init__(self):
        self.deck = self.get_random_deck()
        #self.p1, self.p2 = self.create_decks(win)

    def get_random_deck(self):
        deck = Deck()
        for i in range(3):
            deck.Shuffle()
        return deck

    def create_decks(self):
        player_1 = {}
        player_2 = {}
        index = 0
        down = False
        second_line = 0
        counter = 0

        for_deck_1 = True
        for i in range(16):
            location = Point(122 + 25 * counter, 17 + second_line)
            card = self.dealCard(self.deck, location, down)
            if for_deck_1:
                player_1[index] = [card, location, False]
                player_2[index] = [card, location, True]
                index += 1
            else:
                player_1[index] = [card, location, True]
                player_2[index] = [card, location, False]
                index += 1
            if i == 7:
                second_line = 165
                counter = -1
                for_deck_1 = False
            counter += 1

        new_line = 0
        counter = 0
        down = True
        for i in range(18):
            if down:
                location = Point(121 + 40 * counter, 50 + new_line)
            else:
                location = Point(125 + 40 * counter, 50 + new_line)
                counter += 1

            if i == 9:
                new_line = 30
                counter = 0
            card = self.dealCard(self.deck, location, down)
            player_1[index] = [card, location, down]
            player_2[index] = [card, location, down]
            index += 1
            down = not down

        counter = 0
        new_line = 0
        for i in range(18):
            if down:
                location = Point(121 + 40 * counter, 120 + new_line)
            else:
                location = Point(125 + 40 * counter, 120 + new_line)
                counter += 1

            if i == 7:
                new_line = 30
                counter = 0
            card = self.dealCard(self.deck, location, down)
            player_1[index] = [card, location, down]
            player_2[index] = [card, location, down]
            index += 1
            down = not down
        return player_1, player_2


    def dealCard(self, deck, location, down):
        """Deals a card, draws it and adds it to the dealtCards list, then returns the card, score (value) and the list of total cards"""
        value = deck.Deal()
        card = Card(value,location, down)
        return card

    def clearfromTable(self, dealtCards):
        """Clears all the cards on the table"""
        dealtCards.Undraw()

    def re_draw_card(self, curr_card, location):
        value = curr_card.value
        curr_card.card = curr_card.drawCard(value, location, False)
        win = curr_card.win
        curr_card.re_drawCard(win)

    def draw_card(self, win, curr_card, location, down):
        value = curr_card.value
        curr_card.card = curr_card.drawCard(value, location, down)
        #win = curr_card.win
        curr_card.re_drawCard(win)
    def draw_all_cards(self, win, cards):
        for item in cards:
            self.draw_card(win, cards[item][0], cards[item][1], cards[item][2])

def main():
    deal = {'w': 120, 'h': 60, 'x':30, 'y':30}
    leave = {'w': 120, 'h': 60, 'x':30, 'y':550}
    btns = [Button("Deal", deal['x'], deal['y'], (0, 250, 0), deal['w'], deal['h']),
            Button("Quit", leave['x'], leave['y'], (255, 0, 0), leave['w'], leave['h']),
            Button("Submit 1", 30, 110, (0, 255, 0), 120, 60), Button("Submit 2", 30, 470, (0, 255, 0), 120, 60)]


    width = 1250
    height = 625
    win = pygame.display.set_mode((width, height))
    win.fill((192, 192, 192))

    pygame.display.set_caption("Russi")

    for btn in btns:
        btn.draw(win)
    pygame.display.update()



    run = True
    clock = pygame.time.Clock()
    n = Network()
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
                        n.send('player 1')
    #time.sleep(15)

if __name__ == "__main__":
    main()
