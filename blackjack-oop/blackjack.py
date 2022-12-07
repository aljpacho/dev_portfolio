# TODO: make classes for deck, card, player, hand, dealer, game


# class for card

RANKS = ['2' '3', '4' ,'5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['H', 'C', 'S', 'D']

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def value(self) -> int:
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 1,11
        else:
            return int(self.rank)
    
    def __str__(self) -> str:
        return self.rank + self.suit
