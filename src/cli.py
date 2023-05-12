import sys

from utils.arguments_parser import ParsedInputArguments
from mutator.mutator import Mutator

def version_command():
    python_version = sys.version
    version = '0.0.1'

    print('Guide Selection version: ', version)
    print('Python version: ', python_version)


def resolve_command(args):
    command = args['command']

    if command == 'version':
        version_command()


def main():
    parsed_input = ParsedInputArguments()
    args = parsed_input.arguments

    resolve_command(args)


if __name__ == '__main__':
    main()
