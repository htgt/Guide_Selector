from abc import ABC, abstractmethod

from config.config import Config


class Reader(ABC):
    def __init__(self, config: Config):
        self._config: Config = config

    @abstractmethod
    def read_inputs(self, **kwargs) -> 'Reader':
        """This method returns self."""
        pass
