import sys

from utils.arguments_parser import InputArguments
from mutator.mutator import Mutator


def resolve_command(command):
    print(command)
    

def main():
    parsed_input = InputArguments()
    args = parsed_input.arguments
    command = parsed_input.command

    resolve_command(command)


if __name__ == '__main__':
    main()
