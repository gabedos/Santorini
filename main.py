from board import Board, Space, Worker, BoardAdjacencyIter, NoValidMoves
from players import PlayerFactory

class BoardCLI:

    def __init__(self):
        self._workers = [Worker('A'), Worker('B'), Worker('Y'), Worker('Z')]
        self._board = Board(self._workers)
        self._players = [PlayerFactory(self._board, 1, self._workers[0], self._workers[1]),
                        PlayerFactory(self._board, 2, self._workers[2], self._workers[3])]
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

        try:                                # We'll raise an exception if the player has no valid moves
            while self._board.running:      # Observer checks if any player is standing on a 4 tall piece
                # NEW METHOD, CHECK FOR ANY VALID MOVES, IF NONE EXIST. END THE GAME. OTHER PLAYER WINS... 
                # COULD USE THE ITERATOR I MADE.. COULD ALSO MAKE THE ITERATOR BETTER WITH MORE CONDITION CHECKING?
                self._turn += 1
                self._display_menu()
                self._players[(self._turn + 1) % 2].take_turn()
        except NoValidMoves():
            pass

        if self._turn % 2 == 0:
            print("white has won")
        else:
            print("blue has won")


if __name__ == "__main__":
    BoardCLI().run()