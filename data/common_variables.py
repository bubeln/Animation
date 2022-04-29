class CommonVariables:

    # ---- OBJECT TYPES ----#
    CHARACTER_TYPE = "character"
    ITEM_TYPE = "item"
    LOCATION_TYPE = "location"

    # ---- PRODUCTION JSON KEYS ---- #
    CHARACTERS_KEY = "Characters"
    ITEMS_KEY = "Items"
    NODE_ID_KEY = "WorldNodeId"
    NODE_NAME_KEY = "WorldNodeName"

    # ---- GRAPHICS OBJECT KEYS ---- #
    WIDTH_KEY = "width"
    HEIGHT_KEY = "height"
    CENTER_X_KEY = "center_x"
    CENTER_Y_KEY = "center_y"
    IMAGE_X_KEY = "image_x"
    IMAGE_Y_KEY = "image_y"

    # ---- PATHS ---- #
    BACKGROUND_PATH = "../graphics/backgrounds"
    CHARACTER_PATH = "../graphics/characters"
    GAMEPLAY_PATH = "../productions/gameplay.json"
    OBJECT_PATH = "../graphics/objects"
    SIZE_FILE_PATH = "../data/graphics_size"

    # ---- GRAPHICS SIZE ---- #
    BACKGROUND_WIDTH = 1004
    BACKGROUND_HEIGHT = 710
    #TODO character width and height read as front objects
    CHARACTER_WIDTH = 1426
    CHARACTER_HEIGHT = 2780
    SCENE_WIDTH = 1000
    SCENE_HEIGHT = 720

    ANIMATED_ACTIONS = ["Making a deal ", "Location change ", "Fight ending with character's death "]
    SCALE = 0.1
    ITEM_SCALE = 0.7
