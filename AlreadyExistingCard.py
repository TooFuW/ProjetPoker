

class AlreadyExistingCard(Exception):
    """
        Thrown exception when a card is added in a pack wich already have this card.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def get_card(self):
        return self.card