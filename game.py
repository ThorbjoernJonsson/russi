#File name: game.py
#The class that creates the game. Keeps count of the deck, scores, etc.
#Author Thorbjoern Jonsson
import time
class Game:
    def __init__(self, id):
        self.curr_player = 0
        self.next_play_player = -1
        self.id = id
        self.num_cards_left = 26
        self.moves = [False, False]
        self.last_combo = [False, False]
        self.card_to_flip = [False, False]
        self.score = [0,0]
        self.redraw = False
        self.show_results = True
        self.deck_p0 = []
        self.deck_p1 = []
        self.num_sorts_p0 = [0, 0, 0, 0]
        self.num_sorts_p1 = [0, 0, 0, 0]

    def reset_game(self, deck):
        self.curr_player = 0
        self.next_play_player = -1
        self.moves = [False, False]
        self.last_combo = [False, False]
        self.card_to_flip = [False, False]
        self.redraw = True
        self.show_results = True
        self.num_cards_left = 26
        self.score = [0, 0]
        self.deck_p0, self.deck_p1 =  self.cards_location(deck.shuffledcards)
        self.num_sorts_p0, self.num_sorts_p1 = self.num_on_hand(self.deck_p0, self.deck_p1)

    #Check how many cards of each sort player 0 and player 1 has on their hand. Reason we keep this is because when for
    #example player 0 puts out a heart, player 1 tries to put out something different than a heart but has a heart on
    #hand, we will find out he had an heart on hand by keeping a count on number of cards of each sort on each hand.
    def num_on_hand(self, deck_p0, deck_p1):
        num_p0 = [0, 0, 0, 0]
        num_p1 = [0, 0, 0, 0]
        for i in range(len(deck_p0)):
            if deck_p0[i][2] == 0 and (i <= 7 or (i >= 16 and i <= 33)):
                if deck_p0[i][0][0] == 'h':
                    num_p0[0] += 1
                if deck_p0[i][0][0] == 's':
                    num_p0[1] += 1
                if deck_p0[i][0][0] == 'd':
                    num_p0[2] += 1
                if deck_p0[i][0][0] == 'c':
                    num_p0[3] += 1
            if deck_p1[i][2] == 0 and ((i >= 8 and i <= 15) or i >= 34):
                if deck_p1[i][0][0] == 'h':
                    num_p1[0] += 1
                if deck_p1[i][0][0] == 's':
                    num_p1[1] += 1
                if deck_p1[i][0][0] == 'd':
                    num_p1[2] += 1
                if deck_p1[i][0][0] == 'c':
                    num_p1[3] += 1
        return num_p0, num_p1

    def game_is_finished(self):
        self.show_results = False

    #Update who's turn it is to play.
    def update_next_play_player(self, data):
        temp = data.split(",")
        self.next_play_player = int(temp[1])

    #Runs in the beginning to update the location and if a card should turn up (0) or down (1)
    def cards_location(self, deck):
        player_1 = {}
        player_2 = {}
        index = 0
        down = False
        second_line = 0
        counter = 0
        x_line = 200
        y_line = 5

        for_deck_1 = True
        for i in range(16):
            location = (200 + 75 * counter, y_line)
            if for_deck_1:
                player_1[index] = [deck[index], location, False]
                player_2[index] = [deck[index], location, True]
                index += 1
            else:
                player_1[index] = [deck[index], location, True]
                player_2[index] = [deck[index], location, False]
                index += 1
            if i == 7:
                y_line = 520
                counter = -1
                for_deck_1 = False
            counter += 1

        new_line = 0
        counter = 0
        down = True
        y_line = 110
        for i in range(16,52):
            if down:
                location = (x_line + 100 * counter, y_line)
            else:
                location = (x_line + 10 + 100 * counter, y_line)
                counter += 1

            if i == 25:
                y_line += 100
                counter = 0

            if i == 33:
                y_line += 110
                counter = 0
            if i == 43:
                y_line += 100
                counter = 0
            player_1[index] = [deck[index], location, down]
            player_2[index] = [deck[index], location, down]
            index += 1
            down = not down

        return player_1, player_2

    #When a player puts out a card, we reduce the number of cards of that sort on hand.
    def play(self, card, player):
        temp = card.split(',')
        self.deck_p0[int(temp[0])][1] = (int(temp[1]), int(temp[2]))
        self.deck_p1[int(temp[0])][1] = (int(temp[1]), int(temp[2]))
        self.deck_p0[int(temp[0])][2] = False
        self.deck_p1[int(temp[0])][2] = False
        self.redraw = True
        self.moves[player] = self.deck_p0[int(temp[0])][0]

        card_sort = self.deck_p0[int(temp[0])][0][0]
        number = 0
        if card_sort == 's':
            number = 1
        elif card_sort == 'd':
            number = 2
        elif card_sort == 'c':
            number = 3
        if player == 0:
            self.num_sorts_p0[number] -= 1
        else:
            self.num_sorts_p1[number] -= 1


    def not_redraw(self):
        self.redraw = False

    def update_curr_player(self, p):
        self.curr_player = p

    #Update the number of cards of each sort when cards are flipped.
    def flip_card(self, data, p):
        temp = data.split(',')
        num_card = int(temp[1])
        self.card_to_flip[p] = num_card
        card_sort = 0
        if self.deck_p0[num_card][0][0] == 's':
            card_sort = 1
        elif self.deck_p0[num_card][0][0] == 'd':
            card_sort = 2
        elif self.deck_p0[num_card][0][0] == 'c':
            card_sort = 3
        if p == 0:
            self.num_sorts_p0[card_sort] += 1
        else:
            self.num_sorts_p1[card_sort] += 1

    def connected(self):
        return self.ready

    #Once both cards are out, calcuate
    def update_score(self):

        #Check which player one this round. Also update which player get's do go next based on who won this round.
        play_0_wins = False
        self.next_play_player = 1
        if self.moves[0][0] == self.moves[1][0]:
            vals = [0, 0]
            for i in range(len(vals)):
                if self.moves[i][1:].isdigit():
                    vals[i] = int(self.moves[i][1:])
                    if vals[i] == 1:
                        vals[i] = 14
                else:
                    if self.moves[i][1:] == "j":
                        vals[i] = 11
                    elif self.moves[i][1:] == "q":
                        vals[i] = 12
                    else:
                        vals[i] = 13
            if vals[0] > vals[1]:
                play_0_wins = True
                self.next_play_player = 0
                self.score[0] += 1
            else:
                self.score[1] += 1
        else:
            self.score[self.curr_player] += 1
            if self.curr_player == 0:
                play_0_wins = True
                self.next_play_player = 1

        #Remove the last pair of cards. In Russi you get to see the last pair of cards, the rest you can't look at.
        if self.last_combo[0]:
            for i in range(len(self.deck_p0)):
                if self.deck_p0[i][0] == self.last_combo[0]:
                    self.deck_p0[i][2] = 2
                    self.deck_p1[i][2] = 2
                if self.deck_p0[i][0] == self.last_combo[1]:
                    self.deck_p0[i][2] = 2
                    self.deck_p1[i][2] = 2

        #Check if a card needs to flip and if so update it.
        if self.card_to_flip[0] != False:
            val = self.card_to_flip[0]
            self.deck_p0[val][2] = 0
            self.deck_p1[val][2] = 0
            self.card_to_flip[0] = False
        if self.card_to_flip[1] != False:
            val = self.card_to_flip[1]
            self.deck_p0[val][2] = 0
            self.deck_p1[val][2] = 0
            self.card_to_flip[0] = False

        time.sleep(1)

        #Update the pair locations. If player 0 won it goes up, if player 1 won it goes down.
        coord_x = (910, 520)
        coord_y = (1000, 520)
        if play_0_wins:
            coord_x = (910, 5)
            coord_y = (1000, 5)
        for i in range(len(self.deck_p0)):
            if self.deck_p0[i][0] == self.moves[0]:
                self.deck_p0[i][1] = coord_x
                self.deck_p1[i][1] = coord_x
            elif self.deck_p0[i][0] == self.moves[1]:
                self.deck_p0[i][1] = coord_y
                self.deck_p1[i][1] = coord_y

        self.last_combo[0] = self.moves[0]
        self.last_combo[1] = self.moves[1]
        self.moves[0] = False
        self.moves[1] = False

        #Update number of cards left because when 0 cards left you update the players of who won and who lost
        self.num_cards_left -= 1
