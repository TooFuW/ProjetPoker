from Deck import Deck

my_deck = Deck()

print(my_deck)
print("\n\n")

my_deck.shuffle()

print(my_deck, len(my_deck))
print("\n\n")
print(my_deck.draw(), len(my_deck))