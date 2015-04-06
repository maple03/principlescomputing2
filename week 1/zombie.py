"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
            
    def __str__(self):
        """ 
        Print everything in human-readable format.
        """
        answer = "Grid:\n"
        answer += poc_grid.Grid.__str__(self)
        answer += "Humans: "
        answer += str(self._human_list)
        answer += "\n"
        answer += "Zombies: "
        answer += str(self._zombie_list)
        answer += "\n"
        return answer
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._zombie_list = []
        self._human_list = []
        poc_grid.Grid.clear(self)
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        if self.is_empty(row, col):
            self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        if self.is_empty(row, col):
            self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        distance_field = [[(self._grid_height * self._grid_width) 
                           for _col in range(self._grid_width)] 
                           for _row in range(self._grid_height)]
        boundary = poc_queue.Queue()
        if entity_type == "human":
            for human in self.humans():
                boundary.enqueue(human)
        elif entity_type == "zombie":
            for zombie in self.zombies():
                boundary.enqueue(zombie)
        for cell in boundary:
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
        
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]):
                    if visited.is_empty(neighbor[0], neighbor[1]):
                        visited.set_full(neighbor[0], neighbor[1])
                        boundary.enqueue(neighbor)
                        if distance_field[current_cell[0]][current_cell[1]] + 1 < distance_field[neighbor[0]][neighbor[1]]:
                            distance_field[neighbor[0]][neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
                
        return distance_field 
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for human in list(self._human_list):
            move_away = []
            human_neighbors = self.eight_neighbors(human[0], human[1])
            neighbor_distances = [zombie_distance[neighbor[0]][neighbor[1]] 
                                  for neighbor in human_neighbors
                                  if self.is_empty(neighbor[0], neighbor[1])]
            max_distance = max(neighbor_distances)
            for neighbor in human_neighbors:
                if zombie_distance[neighbor[0]][neighbor[1]] == max_distance:
                    if self.is_empty(neighbor[0], neighbor[1]):
                        move_away.append((neighbor[0], neighbor[1]))
            if zombie_distance[human[0]][human[1]] == max_distance:
                move_away.append((human[0], human[1]))

            self._human_list[self._human_list.index(human)] = random.choice(move_away)
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for zombie in list(self._zombie_list):
            min_distance = human_distance[zombie[0]][zombie[1]]
            move_closer = []
            zombie_neighbors = self.four_neighbors(zombie[0], zombie[1])
            # Strange, but list comprehension doesn't work here
            for neighbor in zombie_neighbors:
                if human_distance[neighbor[0]][neighbor[1]] < min_distance:
                    min_distance = human_distance[neighbor[0]][neighbor[1]]
            for neighbor in zombie_neighbors:
                if human_distance[neighbor[0]][neighbor[1]] == min_distance:
                    if self.is_empty(neighbor[0], neighbor[1]):
                        move_closer.append((neighbor[0], neighbor[1]))
            if human_distance[zombie[0]][zombie[1]] == min_distance:
                move_closer.append((zombie[0], zombie[1]))
            self._zombie_list[self._zombie_list.index(zombie)] = random.choice(move_closer)

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40))
