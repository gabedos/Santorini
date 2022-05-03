import random

from memento import Caretaker
from board import Board, BoardAdjacencyIter, Worker
from memento import Caretaker

HUMAN = 1
RANDOM = 2
HEURISTIC = 3

directionDict = {
    # The change in cord for each direction
    "n":(-1,0),
    "ne":(-1,1),
    "e":(0,1),
    "se":(1,1),
    "s":(1,0),
    "sw":(1,-1),
    "w":(0,-1),
    "nw":(-1,-1)
}

class PlayerFactory:
    def create_player(self, board, pid, w1, w2, player_type = HUMAN):
        player_mapping = {HUMAN: HumanPlayer, RANDOM: RandomPlayer, HEURISTIC: HeuristicPlayer}
        return player_mapping[player_type](board, pid, w1, w2)

class Player:
    
    def __init__(self, board, pid, w1, w2, player_type = HUMAN):
        
        self._workers = [w1, w2]
        self._board = board
        self._pid = pid
        self._player_type = player_type

        self._history = Caretaker(self)

        if self._pid == 1:
            board.move(w1, None, (3,1))
            board.move(w2, None, (1,3))
        else:
            board.move(w1, None, (3,3))
            board.move(w2, None, (1,1))

    def _check_valid_moves(self):
        """Halts execution of the game when the player's workers have no moves"""

        for worker in self._workers:
            for cord in BoardAdjacencyIter(self._board, worker.cord):
                # If any valid adjacent space exists, return without error
                return

        raise NoValidMoves()
    
    def choose_worker(self):
        valid_workers = ["A", "B"]
        invalid_workers = ['Y', "Z"]
        if self._pid == 2:
            valid_workers = ["Y", "Z"]
            invalid_workers = ["A", "B"]

        while True:
            worker_id = input("Select a worker to move\n")
            if worker_id in valid_workers:
                break
            if worker_id in invalid_workers:
                print("That is not your worker")
            else:
                print("Not a valid worker")

        # Get Worker object
        index = 0
        if worker_id == 'B' or worker_id == 'Z':
            index = 1
        worker = self._workers[index]
        
        return worker
    
    def choose_space(self, worker):
        new_space = None
        dir_list = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']

        inputting = True
        while inputting:
            dir_move = input(f"Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
            if dir_move in dir_list:
                new_space = worker.new_space(directionDict.get(dir_move))
                if new_space and self._board.check_heights(worker.cord, new_space) and self._board.is_unoccupied(new_space):
                    inputting = False
                else:
                    print(f"Cannot move {dir_move}")
            else:
                print("Not a valid direction")
        
        return new_space
    
    def choose_build(self, worker, new_space):
        new_space = None
        dir_list = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']

        inputting = True
        while inputting:
            dir_build = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
            if dir_build in dir_list:
                new_space = worker.new_space(directionDict.get(dir_build))
                if new_space and self._board.is_unoccupied(new_space):
                    inputting = False
                else:
                    print(f"Cannot build {dir_build}")
            else:
                print("Not a valid direction")
        
        return new_space

    def take_turn(self):
        """Requests movement & build data from player and execute actions"""

        # Raises NoValidMoves Error to end game
        self._check_valid_moves()

        # Acquire desired worker
        worker = self.choose_worker()

        # Acquire desired location & move
        new_space = self.choose_space(worker)
        self._board.move(worker, worker.cord, new_space)

        # Acquire desired location & build
        new_space = self.choose_build(worker, new_space)
        self._board.build(new_space)

    def list_triples(self):
        list1 = self._list_worker_moves(True)
        list2 = self._list_worker_moves(False)
        return list1 + list2

    def _list_worker_moves(self, is_w1:bool):

        worker = self._workers[0]
        if is_w1:
            worker = self._workers[1]

        start = worker.cord
        movements = []
        # Go through all of workers1 valid spaces and save them
        for move in BoardAdjacencyIter(self._board, start):
            movements.append((worker.id, move))

        complete = []
        # Then go through all of the valid movement spaces and find valid build spaces
        for w, moved in movements:
            for built in BoardAdjacencyIter(self._board, moved, False):
                complete.append((w, moved, built))
            # Edge case: include the tile you were just on as a valid build
            complete.append((w, moved, start))

        # # WIP: still need to call the converter on complete... 
        # # or maybe we can have an adapter class! wooooo

        return complete
    
    def print_move(self, triple, cord1, cord2):
        """cord1 and cord2 are the worker's coordinates"""
        dir1 = (triple[1][0] - cord1, triple[1][1] - cord2)
        dir2 = (triple[2][0] - triple[1][0], triple[2][1] - triple[1][1])
        key1 = list(directionDict.keys())[list(directionDict.values()).index(dir1)]
        key2 = list(directionDict.keys())[list(directionDict.values()).index(dir2)]
        print(triple[0] + "," + key1 + "," + key2)

class HumanPlayer(Player):
    def __init__(self, board, pid, w1, w2):
        super().__init__(board, pid, w1, w2, HUMAN)

class RandomPlayer(Player):
    def __init__(self, board, pid, w1, w2):
        super().__init__(board, pid, w1, w2, RANDOM) # right syntax?

    def take_turn(self):
        # get all possible triples
        triples = self.list_triples()

        # choose a random triple
        random_index = random.randint(0,len(triples)-1)
        triple = triples[random_index]

        # Acquire desired worker
        worker = self._workers[0]
        if triple[0] == 'B' or triple[0] == 'Z':
            worker = self._workers[1]

        # Print to CLI
        self.print_move(triple, worker.cord[0], worker.cord[1])

        # Acquire desired location & move
        self._board.move(worker, worker.cord, triple[1])

        # Acquire desired location & build
        self._board.build(triple[2])


class HeuristicPlayer(Player):
    def __init__(self, board, pid, w1, w2):
        super().__init__(board, pid, w1, w2, RANDOM) # right syntax?

    def calculate_height(self, cord1, cord2):
        h1 = self._board.get_height(cord1)
        h2 = self._board.get_height(cord2)

        # if height = 3, worker wins the game!
        if h1 == 3:
            h1 = float('inf')
        if h2 == 3:
            h2 = float('inf')

        return h1 + h2

    def calculate_center_score(self, cord1, cord2):
        return self._board.get_center_score(cord1) +\
               self._board.get_center_score(cord2)

    def calculate_distance_score(self, cord1, cord2):
        # distance_score for w1
        dist_1 = self._board.get_distance_score(self._pid, cord1)

        # distance_score for w2
        dist_2 = self._board.get_distance_score(self._pid, cord2)

        return 8 - dist_1 - dist_2

    def take_turn(self):
        # get all possible triples
        triples = self.list_triples()

        best_move_score = 0
        best_triple = triples[0]

        # calculate move_score for each triple
        c1 = 6
        c2 = 3
        c3 = 3

        for triple in triples:
            if triple[0] == 'A' or triple[0] == 'Y':
                # moving first worker
                cord1 = triple[1]
                cord2 = self._workers[1].cord
            else:
                # moving second worker
                cord1 = self._workers[0].cord
                cord2 = triple[1]

            height_score = self.calculate_height(cord1, cord2)
            center_score = self.calculate_center_score(cord1, cord2)
            distance_score = self.calculate_distance_score(cord1, cord2)
            move_score = c1*height_score + c2*center_score + c3*distance_score

            if move_score > best_move_score:
                best_move_score = move_score
                best_triple = triple

            # WIP nothing about where you build??
        
        # print(best_triple)

        # Acquire desired worker
        worker = self._workers[0]
        if best_triple[0] == 'B' or best_triple[0] == 'Z':
            worker = self._workers[1]

        # Print to CLI
        self.print_move(best_triple, worker.cord[0], worker.cord[1])

        # Acquire desired location & move
        self._board.move(worker, worker.cord, best_triple[1])

        # Acquire desired location & build
        # WIP THIS IS A LOT OF REPEATED CODE FROM RANDOM PLAYER CLASS
        self._board.build(best_triple[2])

class NoValidMoves(Exception):
    """Raised when the current player has no available moves on either player"""

    def __init__(self):
        self.message = "The player has no valid moves and the game is over"
        super().__init__(self.message)