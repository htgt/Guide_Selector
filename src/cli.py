import sys

from utils.arguments_parser import InputArguments
from mutator.mutator import Mutator


def resolve_command(args):
    command = args['command']

def main():
    parsed_input = InputArguments()
    args = parsed_input.arguments

    resolve_command(args)


if __name__ == '__main__':
    main()
