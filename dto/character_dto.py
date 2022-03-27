class CharacterDTO:

    def __init__(self, character_id, name, items=None):
        self.id = character_id
        self.name = name
        self.items = items
