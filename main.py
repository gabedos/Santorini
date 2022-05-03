import sys

from board import Board, Space, Worker, BoardAdjacencyIter
from players import PlayerFactory, NoValidMoves, RandomPlayer, HeuristicPlayer

HUMAN = 1
RANDOM = 2
HEURISTIC = 3

class BoardCLI:

    def __init__(self, p1_type = HUMAN, p2_type = HUMAN, undo_redo = False, display_score = False):
        self._p1_type = p1_type
        if p1_type == 'random':
            self._p1_type = RANDOM
        elif p1_type == 'heuristic':
            self._p1_type = HEURISTIC

        self._p2_type = p2_type
        if p2_type == 'random':
            self._p2_type = RANDOM
        elif p1_type == 'heuristic':
            self._p2_type = HEURISTIC

        self._undo_redo = False
        if undo_redo == 'on':
            self._undo_redo = True
        
        self._display_score = False
        if display_score == 'on':
            self._display_score = True

        self._workers = [Worker('A'), Worker('B'), Worker('Y'), Worker('Z')]
        self._board = Board(self._workers)
        # self._players = [PlayerFactory(self._board, 1, self._workers[0], self._workers[1], self._p1_type),
        #                 PlayerFactory(self._board, 2, self._workers[2], self._workers[3], self._p2_type)]

        self._players = [HeuristicPlayer(self._board, 1, self._workers[0], self._workers[1]),
                        PlayerFactory(self._board, 2, self._workers[2], self._workers[3], self._p2_type)]

        # player_mapping = {"human": HumanPlayer,
        #         "random": RandomPlayer,
        #         "heuristic": HeuristicPlayer}

        # return player_mapping[player_type](board, pid, w1, w2)

        self._turn = 0

    def _display_menu(self):
        msg = str(self._board)
        col = "white"
        workers = "AB"
        if self._turn % 2 == 0:
            col = "blue"
            workers = "YZ"
        msg += f"\nTurn: {self._turn}, {col} ({workers})"
        print(msg)

    def run(self):

        try:
            # Observer checks if any player is standing on a 4 tall piece
            while self._board.running:
                self._turn += 1
                self._display_menu()
                self._players[(self._turn + 1) % 2].take_turn()
        except NoValidMoves:
            # Termination but other player is the winner, not you
            self._turn += 1

        if (self._turn + 1) % 2 == 0:
            print("white has won")
        else:
            print("blue has won")

if __name__ == "__main__":
    BoardCLI(*sys.argv[1:]).run()