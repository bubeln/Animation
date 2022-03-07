class LocationDTO:

    def __init__(self, id, name, characters=None, items=None):
        self.id = id
        self.name = name
        self.characters = characters
        self.items = items
