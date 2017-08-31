from game_data import Item


class Player:
    def __init__(self, x_coordinate, y_coordinate):
        """
        Creates a new Player.
        :param x: x-coordinate of position on map
        :param y: y-coordinate of position on map
        :return: an object Player located at a position (x_coordinate, y_coordinate) on map
        """
        self.inventory = []
        self.tiredness = 0
        self.x = x_coordinate
        self.y = y_coordinate

    def get_position(self):
        """
        Returns the position of the player as a tuple
        :return: A tuple representing the players location.
        """
        return self.x, self.y

    def get_inventory(self):
        """
        Returns the player's inventory as a list
        :return: A list of the items in the player's inventory
        """
        return self.inventory

    def get_tiredness(self):
        """
        Returns an integer representing the player's tiredness
        :return: An integer coefficient of the player's tiredness
        """
        return self.tiredness

    def move(self, dx, dy):
        """
        Given integers dx and dy, move player to new location (self.x + dx, self.y + dy)
        :param dx: An integer value representing how many units to move along the x-axis
        :param dy: An integer value representing how many units to move along the y-axis
        :return: A tuple representing the player's new position
        """
        self.x += dx
        self.y += dy
        return self.get_position()

    def add_item(self, item):
        """
        Add item to inventory.
        :param item: An item object
        :return: none
        """
        self.inventory.append(item)

    def update_tiredness(self, amount):
        """
        Increases the integer coefficient of the player's tiredness by the given amount
        :param amount: An integer representing how much the player's tiredness has changed
        :return:none
        """
        self.tiredness += amount

    def pop_item(self, name):
        """
        Removes the Item object corresponding to the name of the item from the player's inventory
        :param name: The name of the item
        :return: The removed item object
        Remove item from inventory.
        """
        for index, item in enumerate(self.inventory):
            if name == item.get_name():
                return self.inventory.pop(index)

    def has_item(self, name=None):
        """
        If name is given, checks if the player has the item corresponding to name.
        If name is not given, checks if player has any items in inventory
        :param name: (Optional) String representation of the name of the item
        :return: If the name is given, True if the item exists, False otherwise.
        If the name is not given, True if the player's inventory has item(s), False if
        player's inventory is empty.
        """
        if name is None:
            return bool(self.inventory)
        for item in self.inventory:
            if item.get_name() == name:
                return True
        return False
