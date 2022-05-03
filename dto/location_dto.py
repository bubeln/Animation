class LocationDTO:

    def __init__(self, location_id, name, characters=None, items=None):
        self.id = location_id
        self.name = name
        self.characters = characters
        self.items = items
