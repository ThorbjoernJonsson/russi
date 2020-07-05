import time
class Game:
    def __init__(self, id):
        self.curr_player = 0
        self.id = id
        self.moves = [False, False]
        self.last_combo = [False, False]
        self.card_to_flip = [False, False]
        self.score = [0,0]
        self.redraw = False
        self.deck_p1 = []
        self.deck_p2 = []
        self.num_sorts_p1 = [0, 0, 0, 0]
        self.num_sorts_p2 = [0, 0, 0, 0]

    def reset_game(self, deck):
        self.curr_player = 0
        self.moves = [False, False]
        self.last_combo = [False, False]
        self.card_to_flip = [False, False]
        self.redraw = True
        self.score = [0, 0]
        self.deck_p1, self.deck_p2 =  self.cards_location(deck.shuffledcards)
        self.num_sorts_p1, self.num_sorts_p2 = self.num_on_hand(self.deck_p1, self.deck_p2)

    def num_on_hand(self, deck_p1, deck_p2):
        num_p1 = [0, 0, 0, 0]
        num_p2 = [0, 0, 0, 0]
        for i in range(len(deck_p1)):
            if deck_p1[i][2] == 0 and (i <= 7 or (i >= 16 and i <= 33)):
                if deck_p1[i][0][0] == 'h':
                    num_p1[0] += 1
                if deck_p1[i][0][0] == 's':
                    num_p1[1] += 1
                if deck_p1[i][0][0] == 'd':
                    num_p1[2] += 1
                if deck_p1[i][0][0] == 'c':
                    num_p1[3] += 1
            if deck_p2[i][2] == 0 and ((i >= 8 and i <= 15) or i >= 34):
                if deck_p2[i][0][0] == 'h':
                    num_p2[0] += 1
                if deck_p2[i][0][0] == 's':
                    num_p2[1] += 1
                if deck_p2[i][0][0] == 'd':
                    num_p2[2] += 1
                if deck_p2[i][0][0] == 'c':
                    num_p2[3] += 1
        return num_p1, num_p2



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


    def play(self, card, player):
        temp = card.split(',')
        self.deck_p1[int(temp[0])][1] = (int(temp[1]), int(temp[2]))
        self.deck_p2[int(temp[0])][1] = (int(temp[1]), int(temp[2]))
        self.deck_p1[int(temp[0])][2] = False
        self.deck_p2[int(temp[0])][2] = False
        self.redraw = True
        self.moves[player] = self.deck_p1[int(temp[0])][0]

        card_sort = self.deck_p1[int(temp[0])][0][0]
        number = 0
        if card_sort == 's':
            number = 1
        elif card_sort == 'd':
            number = 2
        elif card_sort == 'c':
            number = 3
        if player == 0:
            self.num_sorts_p1[number] -= 1
        else:
            self.num_sorts_p2[number] -= 1


    def not_redraw(self):
        self.redraw = False

    def update_curr_player(self, p):
        self.curr_player = p

    def flip_card(self, data, p):
        temp = data.split(',')
        num_card = int(temp[1])
        self.card_to_flip[p] = num_card
        card_sort = 0
        if self.deck_p1[num_card][0][0] == 's':
            card_sort = 1
        elif self.deck_p1[num_card][0][0] == 'd':
            card_sort = 2
        elif self.deck_p1[num_card][0][0] == 'c':
            card_sort = 3
        if p == 0:
            self.num_sorts_p1[card_sort] += 1
        else:
            self.num_sorts_p2[card_sort] += 1

    def connected(self):
        return self.ready

    def update_score(self):
        play_1_wins = False
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
                play_1_wins = True
                self.score[0] += 1
            else:
                self.score[1] += 1
        else:
            self.score[self.curr_player] += 1
            if self.curr_player == 0:
                play_1_wins = True

        if self.last_combo[0]:
            for i in range(len(self.deck_p1)):
                if self.deck_p1[i][0] == self.last_combo[0]:
                    self.deck_p1[i][2] = 2
                    self.deck_p2[i][2] = 2
                if self.deck_p1[i][0] == self.last_combo[1]:
                    self.deck_p1[i][2] = 2
                    self.deck_p2[i][2] = 2

        if self.card_to_flip[0] != False:
            val = self.card_to_flip[0]
            self.deck_p1[val][2] = 0
            self.deck_p2[val][2] = 0
            self.card_to_flip[0] = False
        if self.card_to_flip[1] != False:
            val = self.card_to_flip[1]
            self.deck_p1[val][2] = 0
            self.deck_p2[val][2] = 0
            self.card_to_flip[0] = False

        time.sleep(1)

        coord_x = (910, 520)
        coord_y = (1000, 520)
        if play_1_wins:
            coord_x = (910, 5)
            coord_y = (1000, 5)
        for i in range(len(self.deck_p1)):
            if self.deck_p1[i][0] == self.moves[0]:
                self.deck_p1[i][1] = coord_x
                self.deck_p2[i][1] = coord_x
            elif self.deck_p1[i][0] == self.moves[1]:
                self.deck_p1[i][1] = coord_y
                self.deck_p2[i][1] = coord_y

        self.last_combo[0] = self.moves[0]
        self.last_combo[1] = self.moves[1]
        self.moves[0] = False
        self.moves[1] = False
