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
        self._state = state

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
    def __init__(self, player):
        self._future = []   # redo
        self._history = []  # undo
        self._player = player

    def save(self):
        # empty out redo list whenever player takes turn
        self._future = []

        # add move to history list
        self._history.append(self._player.save())
        
    def undo(self):

        # check if there are past moves
        if not len(self._history):
            return

        memento = self._history.pop()

        # add to future list for redos
        self._future.append(memento)

        # call undo method on player
        self._player.undo(memento)

    def redo(self):

        if not len(self._future):
            return

        memento = self._future.pop()
        