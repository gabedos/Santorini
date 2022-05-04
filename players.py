import random

from board import Board, BoardAdjacencyIter, Worker, TurnMemento
# from memento import TurnMemento

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
    """Abstract base class"""
    def __init__(self, board:Board, pid, w1:Worker, w2:Worker):
        
        self._workers = [w1, w2]
        self._board = board
        self._pid = pid

        if self._pid == 1:
            board.move(w1, (3,1))
            board.move(w2, (1,3))
        else:
            board.move(w1, (1,1))
            board.move(w2, (3,3))

    def _check_valid_moves(self):
        """
        Halts execution of the game when the player's workers have no moves
        """

        for worker in self._workers:
            for cord in BoardAdjacencyIter(self._board, worker.cord):
                # If any valid adjacent space exists, return without error
                return

        raise NoValidMoves()
    
    def take_turn(self, _undo_redo):
        """
        Requests movement & build data from player and execute actions
        """

        self._check_valid_moves()

        worker, move_space, build_space = self._input_turn()
        worker_was_space = worker.cord

        self._board.move(worker, move_space)
        self._board.build(build_space)

        if _undo_redo:
            self._board.save(TurnMemento((worker, move_space, build_space, worker_was_space)))

    def _input_turn(self):
        raise NotImplementedError()

    def _list_triples(self):
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

        return complete

    def _print_move(self, triple, cord1, cord2):
        """cord1 and cord2 are the worker's coordinates"""
        dir1 = (triple[1][0] - cord1, triple[1][1] - cord2)
        dir2 = (triple[2][0] - triple[1][0], triple[2][1] - triple[1][1])
        key1 = list(directionDict.keys())[list(directionDict.values()).index(dir1)]
        key2 = list(directionDict.keys())[list(directionDict.values()).index(dir2)]
        print(triple[0] + "," + key1 + "," + key2)

    def calculate_height(self, cord1, cord2):
        h1 = self._board.get_height(cord1)
        h2 = self._board.get_height(cord2)
        return h1 + h2

    def calculate_center_score(self, cord1, cord2):
        return self._board.get_center_score(cord1) + self._board.get_center_score(cord2)

    def calculate_distance_score(self, cord1, cord2):
        dist = self._board.get_distance_score(self._pid, cord1, cord2)
        return 8 - dist
    
    def get_scores(self, cord1, cord2):
        height_score = self.calculate_height(cord1, cord2)
        center_score = self.calculate_center_score(cord1, cord2)
        distance_score = self.calculate_distance_score(cord1, cord2)
        return (height_score, center_score, distance_score)

    def calc_score(self, cord1, cord2):
        """Calculate player score"""
        c1 = 3
        c2 = 2
        c3 = 1
        scores = self.get_scores(cord1, cord2)
        turn_score = c1*scores[0] + c2*scores[1] + c3*scores[2]
        return turn_score

class HumanPlayer(Player):
    def __init__(self, board, pid, w1, w2):
        super().__init__(board, pid, w1, w2)

    def _input_turn(self):
        """
        Prompts and returns the (worker, move_space, build_space)
        """

        # Acquire desired worker, move, and build
        worker = self.choose_worker()
        move_space, relative_move = self.choose_space(worker)
        build_space = self.choose_build(worker, relative_move)

        return (worker, move_space, build_space)

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

        index = 0
        if worker_id == 'B' or worker_id == 'Z':
            index = 1
        worker = self._workers[index]
        
        return worker
    
    def choose_space(self, worker:Worker):
        """"
        Returns coordinates of the new space to move worker
        """
        move_space = None
        dir_list = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']

        inputting = True
        while inputting:
            dir_move = input(f"Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
            if dir_move in dir_list:
                move_space = worker.new_space(directionDict.get(dir_move))
                if move_space and self._board.check_heights(worker.cord, move_space) and self._board.is_unoccupied(move_space):
                    inputting = False
                else:
                    print(f"Cannot move {dir_move}")
            else:
                print("Not a valid direction")

        return (move_space, directionDict.get(dir_move))
    
    def choose_build(self, worker:Worker, movement:tuple):
        """
        Returns coordinates of the space to build
        """
        build_space = None
        dir_list = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']

        inputting = True
        while inputting:
            dir_build = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
            if dir_build in dir_list:
                relative_build = tuple(map(sum, zip(movement, directionDict.get(dir_build))))
                build_space = worker.new_space(relative_build)

                # Check unoccupied (or currently occupied by self)
                if build_space and (self._board.is_unoccupied(build_space) or relative_build == (0,0)):
                    inputting = False
                else:
                    print(f"Cannot build {dir_build}")
            else:
                print("Not a valid direction")
        
        return build_space


class RandomPlayer(Player):
    def __init__(self, board, pid, w1, w2):
        super().__init__(board, pid, w1, w2)

    def _input_turn(self):
        
        # Full sample space of valid moves
        triples = self._list_triples()
        move = triples[random.randint(0,len(triples)-1)]

        worker = self._workers[0]
        if move[0] == 'B' or move[0] == 'Z':
            worker = self._workers[1]

        # Print to CLI
        self._print_move(move, worker.cord[0], worker.cord[1])

        return (worker, move[1], move[2])

class HeuristicPlayer(Player):
    def __init__(self, board, pid, w1, w2):
        super().__init__(board, pid, w1, w2)

    def calculate_height(self, cord1, cord2):
        h1 = self._board.get_height(cord1)
        h2 = self._board.get_height(cord2)

        # if height = 3, worker wins the game!
        if h1 == 3:
            h1 = float('inf')
        if h2 == 3:
            h2 = float('inf')

        return h1 + h2

    def _input_turn(self):
        
        # Full sample space of all the moves
        possible_turns = self._list_triples()

        best_turn_score = 0
        best_turn = possible_turns[0]

        # Calculate move_score for each triple
        for turn in possible_turns:

            if turn[0] == 'A' or turn[0] == 'Y':
                # First coordinate is stored in `turn`
                cord1 = turn[1]

                # Second coordinate is the other worker
                cord2 = self._workers[1].cord
            else:
                # First coordinate is the other worker
                cord1 = self._workers[0].cord

                # Second coordinate is stored in turn
                cord2 = turn[1]
            
            turn_score = self.calc_score(cord1, cord2)

            if turn_score > best_turn_score:
                best_turn_score = turn_score
                best_turn = turn

        worker = self._workers[0]
        if best_turn[0] == 'B' or best_turn[0] == 'Z':
            worker = self._workers[1]

        # Print to CLI
        self._print_move(best_turn, worker.cord[0], worker.cord[1])

        return (worker, best_turn[1], best_turn[2])

class NoValidMoves(Exception):
    """
    Raised when the current player has no available moves on either player
    """

    def __init__(self):
        self.message = "The player has no valid moves and the game is over"
        super().__init__(self.message)