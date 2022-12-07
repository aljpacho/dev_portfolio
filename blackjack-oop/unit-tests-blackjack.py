import unittest

import blackjack


class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = blackjack.Deck()

    def test_deck_generation(self):
        """Check to see if deck generated in the correct order of rank-suit"""
        self.assertEqual(
            [
                "2-Hearts",
                "2-Clubs",
                "2-Spades",
                "2-Diamonds",
                "3-Hearts",
                "3-Clubs",
                "3-Spades",
                "3-Diamonds",
                "4-Hearts",
                "4-Clubs",
                "4-Spades",
                "4-Diamonds",
                "5-Hearts",
                "5-Clubs",
                "5-Spades",
                "5-Diamonds",
                "6-Hearts",
                "6-Clubs",
                "6-Spades",
                "6-Diamonds",
                "7-Hearts",
                "7-Clubs",
                "7-Spades",
                "7-Diamonds",
                "8-Hearts",
                "8-Clubs",
                "8-Spades",
                "8-Diamonds",
                "9-Hearts",
                "9-Clubs",
                "9-Spades",
                "9-Diamonds",
                "10-Hearts",
                "10-Clubs",
                "10-Spades",
                "10-Diamonds",
                "J-Hearts",
                "J-Clubs",
                "J-Spades",
                "J-Diamonds",
                "Q-Hearts",
                "Q-Clubs",
                "Q-Spades",
                "Q-Diamonds",
                "K-Hearts",
                "K-Clubs",
                "K-Spades",
                "K-Diamonds",
                "A-Hearts",
                "A-Clubs",
                "A-Spades",
                "A-Diamonds",
            ],
            self.deck.get_cards(),
        )


if __name__ == "__main__":
    unittest.main()
