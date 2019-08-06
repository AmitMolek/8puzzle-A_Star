import numpy as np
import os

# Used for drawing information we want to see when debugging
DEBUG_MODE = 0

# The goal position of the numbers
goal_position = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0])
# The current position of the numbers
current_position = np.array(range(0, 9))
# Shuffling the positions of the numbers (you know... for the fucking game)
np.random.shuffle(current_position)

# Prints the board
def print_board(number_vector):
    for i in range(1, 10):
        if (i % 3) != 0:
            print(number_vector[i - 1], "| ", end='')
        else:
            print(number_vector[i - 1])

# Returns a copy of np_list with objects at a, b switched
def copy_switch_by_index(a, b, np_list):
    # Creating a copty of np_list so we dont change the original
    copy_np_list = np_list.copy()

    tmp = copy_np_list[a]
    copy_np_list[a] = copy_np_list[b]
    copy_np_list[b] = tmp

    return copy_np_list

# Returns the number of misplaced numbers
def misplaced_numbers_new(vec):
    return np.count_nonzero(goal_position[0:8:1] - vec[0:8:1])

# Returns the number of misplaced numbers
def misplaced_numbers(np_list):
    return np.count_nonzero(goal_position - np_list)

# Returns the total manhattan distance between each number and his goal position
def total_manhattan_distance(np_list):
    # Constructing a grid that each cell is a cord
    # Like 0=(0,0) | 1=(1,0) | 2=(2,0)
    # The cords are (x,y) where (0,0) is cell #0
    distance_grid = np.array([np.array([j, i]) for i in range(3) for j in range(3)])
    # Sum of the total distance
    total_dis = 0

    for i in range(1, 9):
        index, = np.where(np_list==i)

        # The wanted position of each number is represented by ((i-1) % 9)
        # You can check it and see that it gets each number to it's wanted position
        # fuck face...
        wanted_cord = distance_grid[(i-1) % 9]
        current_cord = distance_grid[index[0]]

        # Using the formula |X1 - X2| + |Y1 - Y2|
        dis = np.abs(wanted_cord[0] - current_cord[0]) + np.abs(wanted_cord[1] - current_cord[1])
        total_dis += dis

        if DEBUG_MODE:
            print("#", i, " | ", sep='', end='')
            print("Current Position =", index[0], "|", "Distance =", dis)

    return total_dis

def heuristic_cost(vec):
    return misplaced_numbers_new(vec) + total_manhattan_distance(vec)

class StarNode():

    '''
    This class is a data node for the a* algorithm
    '''

    def __init__(self, position=None, parent=None):
        self.position = position
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent = parent

    # f = g + h
    def calculate_cost(self, g, h):
        self.g = g
        self.h = h
        self.f = g + h

    # >= operator
    def __ge__(self, other):
        return ((self.f > other.f) or (self.f == other.f))

    # > operator
    def __gt__(self, other):
        return (self.f > other.f)

    # <= operator
    def __le__(self, other):
        return ((self.f < other.f) or (self.f == other.f))

    # < operator
    def __lt__(self, other):
        return (self.f < other.f)

    # != operator
    def __ne__(self, other):
        return not self.__eq__(other)

    # == operator
    def __eq__(self, other):
        return np.array_equal(self.position, other.position)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def get_inverse_count(vec):
    inv_count = 0
    for i in range(8):
        for j in range(9):
            if vec[i] != 0 and vec[j] != 0 and vec[i] > vec[j]:
                inv_count += 1
    
    return inv_count

def is_position_solvable(vec):
    return ((get_inverse_count(vec) % 2) == 0)

def astar_min():
    # Creating the open nodes agenda (array)
    agenda = np.empty(0)
    closed_agenda = np.empty(0)

    # If there is no solution for the current position, return None
    if not is_position_solvable(current_position):
        return None

    # Creating the start node and calculating it's cost
    start_node = StarNode(current_position, None)
    start_node.calculate_cost(0, heuristic_cost(start_node.position))

    # Creating the end node with the goal position we later we can compare to it
    end_node = StarNode(goal_position, None)

    # Adding the start node to the agenda
    agenda = np.append(agenda, start_node)

    i_count = 0

    # While the agenda is not empty, meaning there is at least one open node
    while agenda.size > 0:

        # Gets the index of the node with the minimum cost
        current_index = np.argmin(agenda)
        # Gets the actual node using it's index in the agenda
        current_node = agenda[current_index]

        i_count += 1
        #cls()
        print("Iteration", i_count, "Agenda size", agenda.size, "Closed agenda size", closed_agenda.size)
        #print("Start position:", start_node.position)
        #print("Current position:", current_node.position)
        #print("f =", current_node.f, " g =", current_node.g, " h =", current_node.h)

        # Deleting the node from the agenda (closing it, making it inactive, calling it whatever...)
        agenda = np.delete(agenda, current_index)
        closed_agenda = np.append(closed_agenda, current_node)

        # Getting the index of the zero in the number positions
        # It's like the zero is out player
        zero_index = np.where(current_node.position==0)[0][0]

        # The array that will hold the children we want to add
        children = np.empty(0, dtype=StarNode)

        # Checking if we can go UP
        if (zero_index - 3) >= 0:
            new_position = copy_switch_by_index(zero_index, zero_index - 3, current_node.position)
            children = np.append(children, StarNode(new_position, current_node))
        # Checking if we can go DOWN
        if (zero_index + 3) <= 8:
            new_position = copy_switch_by_index(zero_index, zero_index + 3, current_node.position)
            children = np.append(children, StarNode(new_position, current_node))
        # Checking if we can go RIGHT
        if ((zero_index + 1) % 3) > 0:
            new_position = copy_switch_by_index(zero_index, zero_index + 1, current_node.position)
            children = np.append(children, StarNode(new_position, current_node))
        # Checking if we can go LEFT
        if ((zero_index - 1) % 3) < 2:
            new_position = copy_switch_by_index(zero_index, zero_index - 1, current_node.position)
            children = np.append(children, StarNode(new_position, current_node))

        # For every child we calculate it's cost and if it's not already active
        # adding it to the agenda
        for child in children:

            # Calculates the child's cost
            # g = the path depth, h = heuristic cost, f = g + h
            child.calculate_cost(current_node.g + 1, heuristic_cost(child.position))

            # If the child is the goal position, we found a solution!
            if child == end_node:
                return child
            else:
                # If the child is not already open
                if not np.any(agenda==child):
                    if not np.any(closed_agenda==child):
                        agenda = np.append(agenda, child)

'''
TODO:
    - Optimize the algo, takes to long to find the solution
    - When the idiot algo finds the solution, it taks to many steps to win... so
      minimize the steps required to get to the goal position

    - Try different algos ?
'''

'''
try:
    val = astar_min()
    while val is None:
        np.random.shuffle(current_position)
        val = astar_min()

    current_n = val
    index_n = 0
    print("Type", val, "Position", val.position, "Parent", val.parent)
    while current_n is not None:
        print("-------------")
        print("Depth =", index_n)
        #print("f=", current_n.f, "g=", current_n.g, "h=", current_n.h)
        print("Heuristic cost =", heuristic_cost(current_n.position))
        print_board(current_n.position)
        current_n = current_n.parent
        index_n += 1
except:
    print("Failed somehow... :(")
'''

test_arr = np.empty(0)
n1 = StarNode(np.array([1,2,3,4,5,6,7,8,0]), None)

test_arr = np.append(test_arr, n1)

print(test_arr)