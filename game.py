from Deck import*
class Game:
    def __init__(self, id, deck):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0
        self.deck = deck
        self.deck_p1, self.deck_p2 = self.cards_location(deck.shuffledcards)

    def get_random_deck(self):
        deck = Deck()
        for i in range(3):
            deck.Shuffle()
        self.deck = deck

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

    def move_card(self):
        return 1

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, card):
        temp = card.split(',')
        self.deck_p1[0][1] = (int(temp[0]), int(temp[1]))
        self.deck_p2[0][1] = (int(temp[0]), int(temp[1]))
        self.deck_p2[0][2] = False


    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
