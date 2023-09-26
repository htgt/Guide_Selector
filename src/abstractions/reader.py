from abc import ABC, abstractmethod


class Reader(ABC):
    @abstractmethod
    def read_inputs(self, args: dict, **kwargs) -> 'Reader':
        """This method returns self."""
        pass
