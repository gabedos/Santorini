from xmlrpc.client import Boolean


class Board:
    """Manages player & worker interactions with the board's spaces"""

    def __init__(self, workers):
        self._observer = VictoryObserver()
        self._spaces = [[Space((x,y), self._observer) for x in range(5)] for y in range(5)]
        self._workers = workers

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

    def check_heights(self, cord1, cord2):
        """Pass in current coordinates (cord1) and new coordinates (cord2)
        Determines whether the hieght difference is a valid worker move"""

        space1 = self._spaces[cord1[0]][cord1[1]]
        space2 = self._spaces[cord2[0]][cord2[1]]

        if space2 - space1 < 2:
            return True
        return False

    def move(self, worker, old, new):
        """Updates the placement of a worker on the board
        takes the old coordinates (x1,y1) and the new coordinates (x2,y2)"""
        if old != None:
            y, x = old
            self._spaces[y][x].remove_worker()

        y, x = new
        self._spaces[y][x].add_worker(worker)
        worker.move(new)

    def build(self, cord):
        self._spaces[cord[0]][cord[1]].build()

    def is_unoccupied(self, cord):
        return self._spaces[cord[0]][cord[1]].is_unoccupied()


class Space:
    """..."""

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
    """..."""
    def __init__(self, id:str, cord = None):
        """Creates a worker with an id: ABXY, and reference to its space"""
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
    
# WIP: make sure these are right (y,x) or (x,y)?
directionDict = {
    # The change in coor for each direction
    "n":(0,1),
    "ne":(-1,1),
    "e":(-1,0),
    "se":(-1,-1),
    "s":(0,-1),
    "sw":(1,-1),
    "w":(1,0),
    "nw":(1,1)
}


class VictoryObserver():

    def __init__(self):
        self._running = True

    @property
    def running(self):
        return self._running

    def __call__(self, level):
        if level == 3:
            print("at level 3")
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
                candidate = tuple(map(sum, zip(cord, (x,y))))
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
            # Not sure if we want the cords or spaces returned
            #self._spaces.append(board._spaces[x][y])

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


# if __name__ == "__main__":
#     b = Board()
#     print(b)
#     bi = BoardAdjacencyIter(b._spaces, b._spaces[0][0])