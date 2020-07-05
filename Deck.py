#File name: Deck.py
#Creates the Deck that will be used.
#Author Thorbjoern Jonsson
import random

class Deck:
    """A class of a deck of playingcards"""
    def __init__(self):
        self.sorts = ["h","d","s","c"]
        self.numbers = ["1","2","3","4","5","6","7","8","9","10","j","q","k"]
        
        # Empty lists for the cards (ordered and shuffled) to go in
        self.deckofcards = [] 
        self.shuffledcards = [] 

        # This loop creates a list with all 52 playingcards
        for sort in self.sorts:
            for number in self.numbers:
                card = sort + number
                self.deckofcards.append(card)

    def Shuffle(self):
        """Shuffles the deck randomly"""
        self.shuffledcards = self.deckofcards
        random.shuffle(self.shuffledcards)
        # Returns new list with shuffled cards
        return self.shuffledcards

