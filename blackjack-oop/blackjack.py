from random import shuffle

# TODO: make classes for deck, card, player, hand, dealer, game


# class for card


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def value(self) -> int:
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 1, 11
        else:
            return int(self.rank)

    def __str__(self) -> str:
        return self.rank + "-" + self.suit

    def __repr__(self) -> str:
        return f"Card('{self.rank}', '{self.suit}')"


class Deck:
    def __init__(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["Hearts", "Clubs", "Spades", "Diamonds"]

        self.cards = list()

        for rank in ranks:
            for suit in suits:
                self.cards.append(Card(rank, suit))

    def get_cards(self):
        cards = list()
        for card in self.cards:
            cards.append(str(card))
        return cards

    def shuffle(self):
        shuffle(self.cards)

    def draw_card(self) -> Card:
        try:
            card = self.cards.pop()
        except IndexError:
            print("Deck is empty")
        else:
            return card


if __name__ == "__main__":
    test_card = Card("2", "D")
    print(test_card)
    print(test_card)
    deck = Deck()
    # print(deck.get_cards())
    deck.shuffle()
    print(deck.get_cards())
    deck.draw_card()
