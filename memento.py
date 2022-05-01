from abc import ABC, abstractmethod

# Originator == BoardCLI or Board?

class Memento(ABC):
    """
    The Memento interface provides a way to retrieve the memento's metadata,
    such as creation date or name. However, it doesn't expose the Originator's
    state.
    """
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_date(self) -> str:
        pass

class ConcreteMemento(Memento):
    def __init__(self, state):
        self._state = state # A copy of the board

    def get_state(self):
        """
        The Originator uses this method when restoring its state.
        """
        return self._state


class Caretaker():
    """
    The Caretaker doesn't depend on the Concrete Memento class. Therefore, it
    doesn't have access to the originator's state, stored inside the memento. It
    works with all mementos via the base Memento interface.
    """
    def __init__(self, board):
        self._history = []
        self._board = board # saving the board might be hard... maybe save the move to undo/redo it

    def backup(self):
        print("\nCaretaker: Saving Originator's state...")
        self._history.append(self._board.save())
        
    def undo(self) -> None:

        if not len(self._history):
            return

        memento = self._history.pop()
        try:
            self._board.restore(memento)
        except Exception:
            self.undo()
