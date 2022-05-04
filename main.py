import sys

from board import Board, Worker
from players import PlayerFactory, NoValidMoves

HUMAN = 1
RANDOM = 2
HEURISTIC = 3

class BoardCLI:

    def __init__(self, p1_type = HUMAN, p2_type = HUMAN, undo_redo = False, display_score = False):
        self._p1_type = p1_type
        if p1_type == 'human':
            self._p1_type = HUMAN
        elif p1_type == 'random':
            self._p1_type = RANDOM
        elif p1_type == 'heuristic':
            self._p1_type = HEURISTIC

        self._p2_type = p2_type
        if p2_type == 'human':
            self._p2_type = HUMAN
        elif p2_type == 'random':
            self._p2_type = RANDOM
        elif p2_type == 'heuristic':
            self._p2_type = HEURISTIC

        self._undo_redo = False
        if undo_redo == 'on':
            self._undo_redo = True
        
        self._display_score = False
        if display_score == 'on':
            self._display_score = True

        self._workers = [Worker('A'), Worker('B'), Worker('Y'), Worker('Z')]
        self._board = Board(self._workers)

        self._players = [PlayerFactory().create_player(self._board, 1, self._workers[0], self._workers[1], self._p1_type),
                        PlayerFactory().create_player(self._board, 2, self._workers[2], self._workers[3], self._p2_type)]

        self._turn = 0

    def _display_menu(self):
        msg = str(self._board)
        col = "white"
        workers = "AB"
        if self._turn % 2 == 0:
            col = "blue"
            workers = "YZ"
        msg += f"\nTurn: {self._turn}, {col} ({workers})"

        if self._display_score:
            # Player 1
            if self._turn % 2 == 1:
                scores = self._players[0].get_scores(self._workers[0].cord, self._workers[1].cord)
            # Player 2
            else:
                scores = self._players[1].get_scores(self._workers[2].cord, self._workers[3].cord)

            msg = msg + ", " + str(scores)

        print(msg)

    def run(self):
        has_gridlock = False

        try:
            # Observer checks if any player is standing on a 4 tall piece
            while self._board.running:
                self._turn += 1
                self._display_menu()

                while self._undo_redo:
                    choice = input("undo, redo, or next\n")
                    if choice == "undo":
                        if self._board.undo():
                            self._turn -= 1
                        self._display_menu()
                    elif choice == "redo":
                        if self._board.redo():
                            self._turn += 1
                        self._display_menu()
                    elif choice == "next":
                        break

                self._players[(self._turn + 1) % 2].take_turn(self._undo_redo)


        except NoValidMoves:
            # Termination but other player is the winner, not you
            has_gridlock = True

        # Someone has won!
        self._turn += 1
        self._display_menu()

        if has_gridlock:
            self._turn += 1

        if self._turn % 2 == 0:
            print("white has won")
        else:
            print("blue has won")

if __name__ == "__main__":
    BoardCLI(*sys.argv[1:]).run()