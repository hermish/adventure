from game_data import World, Statistics, Exam, Location, Item
from player import Player


class Game:
    def __init__(self, map_name, location_name, item_name, exam_name, x, y, hour, minute, end_hour, end_minute):
        """
        Creates a new Game object, with a world filled with locations that have items within them,
            a player that is created at a given position, a time set at a given time, and an end time
            that determines when the game ends.
        :param map_name: string that gives name of text file in which map data is located
        :param location_name: string that gives name of text file in which location data is located
        :param item_name: string that gives name of text file in which item data is located
        :param exam_name: string that gives name of text file in which item data is located
        :param x: integer value of the x-coordinate on which the player is created
        :param y: integer value of the y-coordinate on which the player is created
        :param hour: integer value of the hour of the time initially set in the game
        :param minute: integer value of the minutes of the time initially set in the game
        :param end_hour: integer value of the hour of the time that the game ends
        :param end_minute: integer value of the minutes of the time that the game ends
        :return:
        '"""
        self.questions = 0
        self.over = False
        self.lost = False
        self.final_exam = Exam(exam_name)
        self.world = World(map_name, location_name, item_name)
        self.player = Player(x, y)
        self.statistics = Statistics(hour, minute, end_hour, end_minute)

    def menu(self):
        """
        Prints out all possible actions and returns a list of all available actions.
        :return: a list of all possible actions
        """
        position = self.player.get_position()
        location = self.world.get_location(position)
        directions = self.world.available_moves(position)
        print(" : ".join(directions))
        menu = []
        if self.player.has_item():
            menu.append("drop")
        if location.has_item():
            menu.append("take")
        if location.has_coffee():
            menu.append("buy")
        menu += ["look", "search", "inventory", "score", "quit"]
        print(" : ".join(menu))
        menu += ["go north", "go south", "go east", "go west"]
        return menu

    def time(self):
        """
        Prints out the current time in the game.
        :return: none
        """
        text = self.statistics.str_time()
        print(text)

    def exam_time(self):
        """
        Prints out the exam time.
        :return: none
        """
        text = self.statistics.str_exam_time()
        print("Your exam is at", text)

    def look(self):
        """
        Prints out the full description of the player's current location.
        :return: none
        """
        position = self.player.get_position()
        location = self.world.get_location(position)
        print(location.get_long_description())

    def search(self):
        """
        Looks for items in the player's current location. Prints which items are in the location, if any.
        :return: none
        """
        position = self.player.get_position()
        location = self.world.get_location(position)
        tiredness = self.player.get_tiredness()
        self.statistics.search(tiredness)
        if location.has_item():
            print("You managed to find the following items:")
            items = location.get_item()
            lst_item = [item.get_name() for item in items]
            str_items = ", ".join(lst_item)
            print(str_items)
        else:
            print("There is nothing here!")

    def move(self, x_dist, y_dist):
        """
        Moves the player position (x,y) to (x + x_dist, y + y_dist).
        Moves the player back to the previous location if the target location is blocked.
        Updates player's statistics.
        Prints out location description.
        :param x_dist:
        :param y_dist:
        :return: none
        """
        position = self.player.move(x_dist, y_dist)
        location = self.world.get_location(position)
        tiredness = self.player.get_tiredness()
        points = location.get_points()
        self.player.update_tiredness(1)
        self.statistics.move(points, tiredness)
        name = location.get_name().upper()
        print(name)
        print(location.get_description())
        if self.world.is_location(position):
            location.visit()
        else:
            self.player.move(-x_dist, -y_dist)

    def inventory(self):
        """
        Determines whether the player has items in their inventory.
        Prints out what items, if any, are in the player's inventory.
        :return: none
        """
        if self.player.has_item():
            inventory = self.player.get_inventory()
            lst_inventory = [item.get_name() for item in inventory]
            str_inventory = ", ".join(lst_inventory)
            print(str_inventory)
        else:
            print("You have no items!")

    def take(self, name):
        """
        Takes an item from the player's current location and puts it inside the player's inventory
        :param name: string representation of the item's name
        :return:none
        """
        position = self.player.get_position()
        location = self.world.get_location(position)
        if location.has_item(name):
            item = location.pop_item(name)
            points = item.get_points()
            self.statistics.add_points(points)
            self.player.add_item(item)
            print("Took", name)
        else:
            print("There is no item", name)

    def drop(self, name):
        """
        Takes an item from the player's inventory and puts it in the player's current location.
        :param name: string representations of the item's name
        :return: none
        """
        position = self.player.get_position()
        location = self.world.get_location(position)
        if self.player.has_item(name):
            item = self.player.pop_item(name)
            points = item.get_points()
            self.statistics.add_points(-points)
            location.add_item(item)
            print("Dropped", name)
        else:
            print("You do not have item", name)

    def score(self):
        """
        Prints out the player's current score
        :return: none
        """
        score = self.statistics.get_score()
        print("Your score is", score)
        print()

    def check(self):
        """
        Checks whether the game has been won or has been lost based on whether the exam has started
        or if all the items are in their required destination.
        :return: none
        """
        position = self.player.get_position()
        inventory = self.player.get_inventory()
        if self.statistics.is_past_exam():
            self.over = True
            self.lost = True
        elif len(inventory) == self.world.get_total_items():
            for item in inventory:
                if item.target != position:
                    break
            else:  # no break
                self.over = True

    def exam(self):
        """
        Runs the exam through the exam class, based on the questions given in the puzzle file.
        :return: True of the player passes, False if they do not.
        """
        print("Your exam is about to begin!")
        print()
        for question in range(self.final_exam.get_length()):
            self.final_exam.administer_question()
            self.final_exam.check_answer()
        return self.final_exam.did_pass()

    def buy(self):
        """
        Replicates buying a coffee. Updates time through the statistic object, and reduces player tiredness.
        :return:
        """
        self.statistics.buy_coffee()
        self.player.update_tiredness(-5)
        print("Bought coffee. Boy that was good!")


def background_information(background_file):
    """
    Reads the background_file to obtain important game messages.
    :param background_file: The name of the file with the background information and
    :return: A dictionary with key representing variable names, values being the text
    """
    info_file = open(background_file, "r")
    background = {}
    line = info_file.readline().rstrip()
    while line:
        key = line
        body = ""
        line = info_file.readline()
        while line != "END\n":
            body += line
            line = info_file.readline()
        background[key] = body
        info_file.readline()
        line = info_file.readline().rstrip()
    return background


def run_game():
    """
    Starts the game itself. Allows the player to recursively replay the game.
    :return: none
    """
    # Input Names (Magic numbers)
    game = Game("map.txt", "locations.txt", "items.txt", "puzzle.txt", 2, 3, 8, 0, 13, 0)
    background = background_information("background.txt")
    # Start of Engine
    direction_tuples = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}
    print(background["INTRODUCTION"])
    game.exam_time()
    print()
    game.move(0, 0)
    while not game.over:
        game.time()
        print("What do you want to do?")
        allowed = game.menu()
        print()
        choice = input("Enter action: ").lower()
        print(choice)
        if choice in allowed:
            if choice.startswith("go"):
                request = choice[3:]
                displacement = direction_tuples[request]
                game.move(*displacement)
            elif choice == "buy":
                game.buy()
                print()
            elif choice == "look":
                game.look()
            elif choice == "inventory":
                game.inventory()
                print()
            elif choice == "score":
                game.score()
            elif choice == "search":
                game.search()
                print()
            elif choice == "take":
                print("Take what?")
                name = input()
                game.take(name)
                print()
            elif choice == "drop":
                game.inventory()
                print("Drop what?")
                name = input()
                game.drop(name)
                print()
            elif choice == "quit":
                print("Game over!")
                break
        else:
            print("That action is not allowed here!")
            print()
        game.check()
    else:  # no break
        if game.lost:
            print(background["DEFEAT"])
        else:
            if game.exam():
                print(background["VICTORY"])
            else:
                print(background["DEFEAT"])
    game.score()
    print("Do you want to play again?")
    print("yes : no")
    user_ultimatum = input()
    if user_ultimatum == "yes":
        run_game()


if __name__ == "__main__":
    run_game()
