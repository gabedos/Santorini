from board import Board, Worker

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
    
    def __init__(self, board, pid, w1, w2, type = HUMAN):
        self._workers = [w1, w2]
        self._board = board
        self._pid = pid

        if self._pid == 1:
            board.move(w1, None, (3,1))
            board.move(w2, None, (1,3))
        else:
            board.move(w1, None, (3,3))
            board.move(w2, None, (1,1))


    def _valid_move(self):

        return True

    def take_turn(self):
        """Requests data from player and returns a tuple:
        (Worker, MovementDirection, BuildingDirection)"""

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

        new_space = None
        dir_list = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        while True:
            dir_move = input(f"Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
            if dir_move in dir_list:
                # get coordinates of new space
                new_space = worker.new_space(directionDict.get(dir_move))

                # send heights to board
                if self._board.check_heights(worker.cord, new_space):
                    break
                else:
                    print(f"Cannot move {dir_move}")
            else:
                print("Not a valid direction")

        # MOVE THE WORKER
        self._board.move(worker, worker.cord, new_space)

        while True:
            dir_build = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
            if dir_build in dir_list:
                if worker.new_space(directionDict.get(dir_build)) and True:
                    break
                else:
                    print(f"Cannot build {dir_build}")
            else:
                print("Not a valid direction")

        # BUILD ON THE SPACE


class HumanPlayer(PlayerFactory):
    pass

class HeuristicPlayer(PlayerFactory):
    pass

class RandomPlayer(PlayerFactory):
    pass



# Create an adapter between human moves and robot moves
# So we can then call the same functions on them?