import argparse

class ParsedInputArguments:
    def __init__(self) -> None:
        self.arguments = []
        self.command = ''

        self.parse_arguments()

    def set_args(self, values) -> None:
        self.arguments = values
        self.command = self.arguments['command']

    def parse_arguments(self) -> dict:
        parser = argparse.ArgumentParser(description='Guide Selection CLI')

        parser.add_argument('command',
            help=(
                'Command to run in Guide Selection CLI, available commands: '
                'version, mutator'
            ),
            type=str,
            default='version'
        )
        parser = add_input_args(parser)

        parser = add_input_args(parser)

        self.set_args(vars(parser.parse_args()))


def add_input_args(parser):
        return parser
