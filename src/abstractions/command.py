from abc import ABC, abstractmethod

from config.config import Config


class Command(ABC):

    def __init__(self, config: Config):
        self._config: Config = config

    @abstractmethod
    def run(self, **kwargs):
        pass
