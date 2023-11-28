from abstractions.command import Command
from config.config import Config
from guide_selector import GuideSelector
from mutator.mutator import Mutator
from retriever.retriever import Retriever
from utils.arguments_parser import InputArguments


def main() -> None:
    parsed_input = InputArguments()
    config = Config(parsed_input)

    command = _get_command(config)
    command.run()


def _get_command(config: Config) -> Command:
    if config.command == "retrieve":
        return Retriever(config)
    if config.command == "mutator":
        return Mutator(config)
    if config.command == "guide_selector":
        return GuideSelector(config)


if __name__ == '__main__':
    main()
