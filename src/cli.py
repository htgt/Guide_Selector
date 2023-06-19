import sys

from utils.arguments_parser import InputArguments
from mutator.mutator import Mutator
from mutator.guide import GuideSequence


def resolve_command(command: str, args: dict) -> None:
    if command == "window":
        guide = GuideSequence(args["seq"], args["strand"], args["window_length"])

        print(guide.window)
    

def main() -> None:
    parsed_input = InputArguments()
    args = parsed_input.arguments
    command = parsed_input.command

    resolve_command(command, args)


if __name__ == '__main__':
    main()
