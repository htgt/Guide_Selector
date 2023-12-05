from abstractions.command import Command
from config.config import Config
from mutator.mutator import Mutator
from retriever.retriever import Retriever


class GuideSelector(Command):
    def __init__(self, config: Config):
        super().__init__(config)

    def run(self, **kwargs):
        retriever = Retriever(self._config)
        retriever.run()

        mutator = Mutator(self._config)
        mutator.run(retriever.guide_sequences)
