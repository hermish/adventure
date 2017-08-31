class World:
    def __init__(self, mapdata, locdata, itemdata):
        """
        Creates a new World object, with a map, and data about every location and item in this game world.
        :param mapdata: name of text file containing map data in grid format
            (integers represent each location, separated by space)
            map text file MUST be in this format.
                E.g.
                1 -1 3
                4 5 6
            Where each number represents a different location, and -1 represents an invalid, inaccessible space.
        :param locdata: name of text file containing location data (format left up to you)
        :param itemdata: name of text file containing item data (format left up to you)
        :return: A world object containing a list or lists representing the maps and a dictionary of locations
            keyed to a tuple representing its position. The
        """
        self.map = []
        self.locations = {}
        self.blocked = None
        self.total_items = 0
        self.load_map(mapdata)
        self.load_locations(locdata)
        self.load_items(itemdata)

    def load_map(self, filename):
        """
        Store map from filename (map.txt) in the variable "self.map" as a nested list of strings OR integers like so:
            1 2 5
            3 -1 4
        becomes [['1','2','5'], ['3','-1','4']] OR [[1,2,5], [3,-1,4]]
        RETURN THIS NEW NESTED LIST.
        :param filename: string that gives name of text file in which map data is located
        :return: return nested list of strings/integers representing map of game world as specified above
        """
        map_file = open(filename, "r")
        for line in map_file:
            string_row = line.split()
            int_row = [int(number) for number in string_row]
            self.map.append(int_row)
        map_file.close()
        return self.map

    def load_locations(self, filename):
        """
        Makes a new Location object for each location in filename.
        Stores each Location object in the dictionary self.locations with the key being.
        a tuple representation of the location's position on the map, and the value being
        the Location object at that position.
        :param filename: string that gives the name of the text file in which location data is located
        :return: none
        """
        location_file = open(filename, "r")
        blocked = location_file.readline().rstrip()
        points = int(location_file.readline().rstrip())
        coffee = bool(location_file.readline().rstrip())
        short_description = location_file.readline()
        description_list = []
        line = location_file.readline()
        while line != "END":
            description_list.append(line)
            line = location_file.readline().rstrip()
        long_description = " ".join(description_list)
        self.blocked = Location(blocked, points, coffee, short_description, long_description)
        location_file.readline()
        line = location_file.readline().rstrip()
        while line:
            number = int(line.strip("LOCATION "))
            position = self.get_coordinates(number)
            name = location_file.readline().rstrip()
            points = int(location_file.readline().rstrip())
            coffee = bool(location_file.readline().rstrip())
            short_description = location_file.readline()
            # Long description
            long_description = ""
            line = location_file.readline()
            while line != "END\n":
                long_description += line
                line = location_file.readline()
            # Create location object
            self.locations[position] = Location(name, points, coffee, short_description, long_description)
            # Clean up!
            location_file.readline()
            line = location_file.readline().rstrip()
        location_file.close()

    def load_items(self, filename):
        """
        Makes a new Item object for each item in filename
        Store all Item objects in a position in a list within a Location object corresponding
        to that position.
        Sets self.total_items equal to the number of items in filename
        :param filename: string that gives the name of the text file in which item data is located
        :return: none
        """
        item_file = open(filename, "r")
        line = item_file.readline().rstrip()
        while line:
            position_number = int(line.strip("ITEM "))
            position = self.get_coordinates(position_number)
            name = item_file.readline().rstrip()
            points = int(item_file.readline().rstrip())
            target_number = int(item_file.readline().rstrip())
            target = self.get_coordinates(target_number)
            description = item_file.readline().rstrip()
            # Add item
            self.locations[position].add_item(Item(name, points, target, description))
            self.total_items += 1
            # Clean up!
            item_file.readline()
            item_file.readline()
            line = item_file.readline().rstrip()
        item_file.close()

    def get_total_items(self):
        """
        :return: integer number of the total items
        """
        return self.total_items

    def get_location(self, position):
        """
        Determines whether the location at position exists.
        If it exists, returns the Location object corresponding to that position.
        :param position: Tuple representing a position on the map
        :return: Location object corresponding to the tuple representation of position on
        the map
        """
        if self.is_location(position):
            return self.locations[position]
        return self.blocked

    def get_coordinates(self, index):
        """
        :param index: A non-negative integer value corresponding to a location in the map.
        :return: A tuple representing the coordinates of the location.
        Given a number, returns a tuple representing its position in the world map.
        """
        for y_value, row in enumerate(self.map):
            if index in row:
                x_value = row.index(index)
                return x_value, y_value

    def is_location(self, position):
        """
        Determines whether a Location object exists at the given position
        :param position: Tuple representation of the position on the world map
        :return: True if a Location object exists at the given position. False otherwise.
        """
        return position in self.locations

    def available_moves(self, position):
        """
        Determines the directional moves available at a given position
        :param position: Tuple representation of a position on the map
        :return: List of directional actions available to a player at the given position
        """
        directions = []
        x_pos, y_pos = position
        if self.is_location((x_pos, y_pos - 1)):
            directions.append("go north")
        if self.is_location((x_pos, y_pos + 1)):
            directions.append("go south")
        if self.is_location((x_pos - 1, y_pos )):
            directions.append("go west")
        if self.is_location((x_pos + 1, y_pos)):
            directions.append("go east")
        return directions


class Location:
    def __init__(self, name, points, coffee, short_description, long_description):
        """
        Creates a new Location object, with a name, points, ability to purchase coffee, a short description
        of location and a long description of location
        :param name: string name of location
        :param points: int number of points received for visiting the location
        :param coffee: bool value, True if player can buy coffee, False if player cannot buy coffee
        :param short_description: string short description of location
        :param long_description: string long descriptino of location
        :return: Location object containing a list of items in location
        """
        self.visited = False
        self.items = []
        self.name = name
        self.points = points
        self.coffee = coffee
        self.short = short_description
        self.long = long_description

    def get_name(self):
        """
        Gets the name of the location
        :return: A string with the name of the location.
        """
        return self.name

    def get_points(self):
        """
        Gets the points given when visiting a location for the first time.
        :return: Integer value of points if a player visits the location for the first time.
        If player has visited location before, returns integer value of 0
        """
        if self.visited:
            return 0
        else:
            return self.points

    def get_item(self):
        """
        Gets the list of items available at the location
        :return: A list of all items available at the location
        """
        return self.items

    def get_long_description(self):
        """
        Gets the long description of the location
        :return: A string of the long description of the location
        """
        return self.long

    def get_description(self):
        """
        Gets a description of the location depending on whether the player has
        visited the location or not
        :return: A string with a description of the location
        Returns a short description if it has been visited by the player or a long one if it hasn't.
        """
        if self.visited:
            return self.short
        else:
            return self.long

    def has_coffee(self):
        """
        Determines whether the location has coffee
        :return: True if the location has coffee, false otherwise
        """
        return self.coffee

    def has_item(self, name=None):
        """
        :param name: (Optional) String representation of the name of an item
        :return: If a name is given, returns True if the item name is in the location.
        Returns False if the item name is not in the location.
        If a name is not given, returns True if there are item(s) in the location.
        Returns False if there are no items in the location.
        """

        if name is None:
            return bool(self.items)
        for item in self.items:
            if item.get_name() == name:
                return True
            return False

    def visit(self):
        """
        Notes that the location has been visited before
        :return: none
        """
        self.visited = True

    def add_item(self, item):
        """
        :param item: An item object.
        :return: None
        Adds the item to the location.
        """
        self.items.append(item)

    def pop_item(self, name):
        """
        Returns item object with name, if it exists
        :param name: The name of the item.
        :return: The item object corresponding the specified name.
        """
        for index, item in enumerate(self.items):
            if item.get_name() == name:
                return self.items.pop(index)


class Item:
    def __init__(self, name, points, target, description):
        """
        Creates a new Item object, with a name of item, number of points received for taking the item,
        ,the target location to bring the items, and a description
        :param name: string name of item
        :param points: int value of points received if the item is taken
        :param target: tuple representing the position on the map the item must be brought to
        :param description: string description of the item
        :return: an Item object
        """
        self.name = name
        self.points = points
        self.target = target
        self.description = description

    def get_name(self):
        """
        Gets the name of the item
        :return: A string representing the name of the item.
        """
        return self.name

    def get_points(self):
        """
        Gets the points given to player if player takes the item
        :return: An int value of points received if item is taken
        """
        return self.points

    def get_target_position(self):
        """
        Gets the position on the map that the item must be taken to
        :return: A tuple representing the position on the map of the target destination.
        """
        return self.target


class Statistics:
    def __init__(self, current_hour, current_minute, exam_hour, exam_minute):
        """
        :param current_hour: The current in-game hour
        :param current_minute: The current in-game minute
        :param exam_hour: The hour of the exam
        :param exam_minute:The minute the exam starts
        :return: a Statistics object
        """
        self.score = 0
        self.moves = 0
        self.hour = current_hour
        self.minute = current_minute
        self.exam_hour = exam_hour
        self.exam_minute = exam_minute

    def get_score(self):
        """
        Get's the player's score
        :return: integer value of the player's score
        """
        return self.score

    def add_time(self, minutes):
        """
        :param minutes: The number of minutes to add
        :return: none
        """
        minute_buffer = self.minute + minutes
        add_hour, minute = divmod(minute_buffer, 60)
        self.hour += add_hour
        self.minute = minute

    def add_points(self, points):
        """
        Adds points to the player's current score
        :param points: integer value of points to add to the player's score
        :return: none
        """
        self.score += points

    def is_past_exam(self):
        """
        Determines whether the time has passed beyond the exam time
        :return: True if the current time is past the exam time, False otherwise
        """
        if self.hour < self.exam_hour:
            return False
        if self.minute < self.exam_minute:
            return False
        return True

    def str_time(self):
        """
        Returns the current time in the format HH:MM
        :return: string representation of the current time
        """
        return "{0}:{1:02}".format(self.hour, self.minute)

    def str_exam_time(self):
        """
        Returns the exam time in the format HH:MM
        :return: string representation of the exam time
        """
        return "{0}:{1:02}".format(self.exam_hour, self.exam_minute)

    def move(self, points, tiredness):
        """
        Updates the player's statistics once he or she moves.
        :param points: Integer value of the points to be added to the score
        :param tiredness: Integer value of the player's tiredness coefficient.
        :return: none
        """
        self.moves += 1
        self.score += points
        self.add_time(tiredness)

    def search(self, tiredness):
        """
        Updates the player's statistics after they move.
        :param tiredness: The player's tiredness coefficient
        :return: none
        """
        self.add_time(tiredness + 10)

    def buy_coffee(self):
        """
        Adds amount of time required to buy a coffee.
        The wait time depend on how close the time is to the hour (when places are historically busier).
        :return: none
        """
        distance = abs(30 - self.minute)
        if distance < 10:
            total_time = 10
        elif distance < 20:
            total_time = 5
        else:
            total_time = 15
        self.add_time(total_time)


class Exam:
    def __init__(self, examdata):
        """
        :param examdata: The file name of the exam questions and answers.
        :return: An Exam object.
        """
        self.exam = []
        self.number = 0
        self.correct = 0
        self.incorrect = 0
        self.load_exam(examdata)

    def load_exam(self, examdata):
        """
        :param examdata: The name of the exam file.
        :return: none
        """
        exam_file = open(examdata, "r")
        line = exam_file.readline().rstrip()
        while line:
            question_text = exam_file.readline().rstrip()
            answer = exam_file.readline().rstrip()
            self.exam.append((question_text, answer))
            exam_file.readline()
            exam_file.readline()
            line = exam_file.readline().rstrip()
        exam_file.close()

    def get_length(self):
        """
        :return: The integral length of the exam (in questions)
        """
        return len(self.exam)

    def administer_question(self):
        """
        :return: Poses a question.
        """
        pair = self.exam[self.number]
        text = "QUESTION {0}\n{1}".format(self.number, pair[0])
        print(text)

    def check_answer(self):
        """
        Gets input and checks if that is the answer to the current question.
        Updates number of correct and incorrect answers.
        :return: none
        """
        pair = self.exam[self.number]
        self.number += 1
        print("Enter answer below:")
        answer = input()
        if answer == pair[1]:
            self.correct += 1
        else:
            self.incorrect += 1

    def did_pass(self):
        """
        :return: A boolean representing whether the player passed or failed the exam.
        """
        return self.correct / (self.correct + self.incorrect) > 0.5
