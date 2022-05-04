class TurnMemento:
    def __init__(self, turn_log):
        self._turn = turn_log

    def get_turn(self):
        return self._turn


class Caretaker():
    """
    Manages the TurnMementos
    """
    def __init__(self, player):
        self._future = []   # redo
        self._history = []  # undo
        self._player = player

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
        self._player.undo_turn(memento)
        return True

    def redo(self):

        if len(self._future) == 0:
            return False
        memento = self._future.pop()
        # Re-add to history list for re-undos
        self._history.append(memento)
        self._player.redo_turn(memento)
        return True