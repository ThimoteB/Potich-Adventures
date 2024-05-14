""" This file contains the Player class."""
from classes.card import Card


class Player:
    """Classe représentant un joueur (il y en aura 4)
    On doit donc avoir le numéro du joueur (1,2,3,4)
    Sa liste de cartes ( 4 maximum)
    """

    def __init__(self, number: int):
        # Automatically attributes a number to a new player
        self.number = number
        self.cards = []

    def add_card(self, card: Card):
        """This function is used to add a card to the player's hand.

        Args:
            card (Card): represents the card to add
        """
        self.cards.append(card)
