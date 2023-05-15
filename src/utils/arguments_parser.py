from argparse import ArgumentParser


class InputArguments:
    def __init__(self) -> None:
        self.arguments = {}
        self.command = ''

        self.parse_arguments()

    def set_args(self, values) -> None:
        self.arguments = values
        self.command = self.arguments['command']

    def parse_arguments(self) -> dict:
        parser = ArgumentParser(
            description='Guide Selection CLI',
            prog='Guide Selection'
        )

        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s 0.0.1'
        )
        parser = add_input_args(parser)

        self.set_args(vars(parser.parse_args()))


def add_input_args(parser) -> ArgumentParser:
    return parser
