# from memento import Caretaker, TurnMemento

class Board:
    """Manages player & worker interactions with the board's spaces"""

    def __init__(self, workers):
        self._observer = VictoryObserver()
        self._spaces = [[Space((x,y), self._observer) for x in range(5)] for y in range(5)]
        self._workers = workers
        self._caretaker = Caretaker(self)

    def __str__(self):
        """Formats the board"""
        sep = "+--+--+--+--+--+"
        msg = ""
        for row in self._spaces:
            msg += sep
            msg += '\n'
            for space in row:
                msg += str(space)
            msg += '|'
            msg += '\n'
        msg += sep
        return msg

    @property
    def running(self):
        return self._observer.running

    def get_height(self, cord):
        return self._spaces[cord[0]][cord[1]].level

    def get_center_score(self, cord):
        return Space.pos_rank[cord]

    def get_distance(self, cord1, cord2):
        """Calculating Chebyshev distance between two pieces"""
        return max(abs(cord1[0] - cord2[0]), abs(cord1[1] - cord2[1]))

    def get_distance_score(self, pid, cord1, cord2):
        """Pass in the worker:pid and the two coordinates."""
        # If pid = 1, compare to Y/Z
        if pid == 1:
            # Find minimum distance to Y
            dist11 = self.get_distance(self._workers[2].cord, cord1)
            dist12 = self.get_distance(self._workers[2].cord, cord2)

            # Find minimum distance to Z
            dist21 = self.get_distance(self._workers[3].cord, cord1)
            dist22 = self.get_distance(self._workers[3].cord, cord2)
        # If pid = 2, compare to A/B
        else:
            # Find minimum distance to A
            dist11 = self.get_distance(self._workers[0].cord, cord1)
            dist12 = self.get_distance(self._workers[0].cord, cord2)

            # Find minimum distance to B
            dist21 = self.get_distance(self._workers[1].cord, cord1)
            dist22 = self.get_distance(self._workers[1].cord, cord2)

        return min(dist11, dist12) + min(dist21, dist22)

    def check_heights(self, cord1, cord2):
        """Pass in current coordinates (cord1) and new coordinates (cord2)
        Determines whether the height difference is a valid worker move"""

        space1 = self._spaces[cord1[0]][cord1[1]]
        space2 = self._spaces[cord2[0]][cord2[1]]

        if space2 - space1 < 2:
            return True
        return False

    def move(self, worker, new):
        """Updates the placement of a worker on the board
        takes the old worker coordinates (x1,y1) and the new coordinates (x2,y2)"""

        if worker.cord != None:
            y, x = worker.cord
            self._spaces[y][x].remove_worker()

        y, x = new
        self._spaces[y][x].add_worker(worker)
        worker.move(new)

    def build(self, cord):
        self._spaces[cord[0]][cord[1]].build()

    def unbuild(self, cord):
        self._spaces[cord[0]][cord[1]].unbuild()

    def is_unoccupied(self, cord):
        return self._spaces[cord[0]][cord[1]].is_unoccupied()

    def save(self, turn_memento):
        self._caretaker.save(turn_memento)

    def undo(self):
        return self._caretaker.undo()

    def undo_turn(self, turn_memento):
        worker, move_space, build_space, was_space = turn_memento.get_turn()
        self.move(worker, was_space)
        self.unbuild(build_space)

    def redo(self):
        return self._caretaker.redo()

    def redo_turn(self, turn_memento):
        worker, move_space, build_space, was_space = turn_memento.get_turn()
        self.move(worker, move_space)
        self.build(build_space)


class Space:
    """Stores the data for the board's space"""

    # center = 2, ring = 1, edge = 0
    pos_rank = {
        (0, 0): 0,
        (1, 0): 0,
        (2, 0): 0,
        (3, 0): 0,
        (4, 0): 0,
        (0, 1): 0,
        (1, 1): 1,
        (2, 1): 1,
        (3, 1): 1,
        (4, 1): 0,
        (0, 2): 0,
        (1, 2): 1,
        (2, 2): 2,
        (3, 2): 1,
        (4, 2): 0,
        (0, 3): 0,
        (1, 3): 1,
        (2, 3): 1,
        (3, 3): 1,
        (4, 3): 0,
        (0, 4): 0,
        (1, 4): 0,
        (2, 4): 0,
        (3, 4): 0,
        (4, 4): 0
    }

    def __init__(self, cord, observer):
        # Tuple (x,y)
        self._cord = cord
        # Reference to the Worker
        self._worker = None
        # Int 0-4
        self._level = 0
        self._observer = observer
        self._rank = Space.pos_rank.get(cord)

    def __str__(self):
        worker = " "
        if self._worker:
            worker = str(self._worker)
        return f"|{self._level}{worker}"

    def remove_worker(self):
        self._worker = None

    def add_worker(self, worker):
        self._worker = worker
        self._notify()

    def _notify(self):
        self._observer(self._level)

    def is_unoccupied(self):
        if self._worker or self._level == 4:
            return False
        else:
            return True

    def build(self):
        self._level += 1
        # assert(self._worker == None)
        # assert(self._level <= 4)

    def unbuild(self):
        self._level -= 1
        # assert(self._worker == None)
        # assert(self._level >= 0)

    def __sub__(self, other):
        return self._level - other._level

    @property
    def cord(self):
        return self._cord

    @property
    def level(self):
        return self._level

    @property
    def rank(self):
        return self._rank


class Worker:
    """
    Worker class used to represent workers on the board
    """
    def __init__(self, id:str, cord = None):
        """
        Creates a worker with an id: ABXY, 
        and reference to its space
        """
        self._id = id
        self._cord = cord

    def __str__(self):
        return str(self._id)

    def move(self, new_cord):
        self._cord = new_cord

    def new_space(self, movement):
        """"Determines whether a move on a worker is valid.
        If its valid, then returns new coordinates. Otherwise False"""
        x,y = map(sum, zip(movement, self._cord))
        if x < 0 or x > 4 or y < 0 or y > 4:
            return False
        return (x,y)

    @property
    def cord(self):
        return self._cord
    
    @property
    def id(self):
        return self._id


class VictoryObserver():

    def __init__(self):
        self._running = True

    @property
    def running(self):
        return self._running

    def __call__(self, level):
        if level == 3:
            # print("at level 3")
            self._running = False


class BoardAdjacencyIter:
    """Returns an iterable of a space's valid adjacent spaces"""
    
    def __init__(self, board:Board, cord:tuple, type:bool = True):
        """type = True will check height differences for workers movement.
        type = False will only check if the spaces are unoccupied"""

        adj_cords = []

        # Loop through 8 possible moves
        for x in range(-1,2):
            for y in range(-1,2):
                
                # Don't include the original space itself
                if x == 0 and y == 0:
                    continue

                # Check if within bounds of the board
                if cord[0]+y > 4 or cord[0]+y < 0:
                    continue
                if cord[1]+x > 4 or cord[1]+x < 0:
                    continue

                # Determining whether a worker can move to candidate from original
                candidate = tuple(map(sum, zip(cord, (y,x))))
                if type:
                    if not board.check_heights(cord, candidate):
                        continue
                if not board.is_unoccupied(candidate):
                    continue

                adj_cords.append(candidate)

        self._spaces = []
        self._index = 0
        for y,x in adj_cords:
            self._spaces.append((y,x))

    def __next__(self):
        if self._index == len(self._spaces):
            raise StopIteration()
        space = self._spaces[self._index]
        self._index += 1
        return space

    def __iter__(self):
        return self
    
    @property
    def spaces(self):
        return self._spaces


class TurnMemento:
    def __init__(self, turn_log):
        self._turn = turn_log

    def get_turn(self):
        return self._turn

class Caretaker:
    """
    Manages the TurnMementos
    """
    def __init__(self, board:Board):
        self._future = []   # redo
        self._history = []  # undo
        self._board = board

    def save(self, turn_memento):
        """
        Saves a turn log containing:
        (worker, move_space, build_space, was_space)
        """

        # Empty out redo list whenever player takes turn
        self._future = []
        self._history.append(turn_memento)
        
    def undo(self):

        # check if there are past moves (WIP DO WE NEED TO DO SOMETHING WHEN UNDO NOT POSSIBLE?)
        if len(self._history) == 0:
            return False
        memento = self._history.pop()
        # Add to future list for redos
        self._future.append(memento)
        self._board.undo_turn(memento)
        return True

    def redo(self):

        if len(self._future) == 0:
            return False
        memento = self._future.pop()
        # Re-add to history list for re-undos
        self._history.append(memento)
        self._board.redo_turn(memento)
        return True