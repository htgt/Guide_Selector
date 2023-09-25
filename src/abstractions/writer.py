from abc import ABC, abstractmethod


class Writer(ABC):
    @abstractmethod
    def write_outputs(self, output_dir: str):
        pass
