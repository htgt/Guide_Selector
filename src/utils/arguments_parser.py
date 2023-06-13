from argparse import ArgumentParser


class InputArguments:
    def __init__(self) -> None:
        self.arguments = {}
        self.command = ''

        self.parse_arguments()

    def set_args(self, values) -> None:
        self.arguments = values
        self.command = values['dest']

    def parse_arguments(self) -> dict:
        parser = ArgumentParser(
            description='Guide Selection CLI',
            prog='Guide Selection'
        )

        self._add_window_command_parser(parser)

        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s 0.0.1'
        )
        parser = add_input_args(parser)

        self.set_args(vars(parser.parse_args()))

    def _add_window_command_parser(self, parser) -> None:
        subparsers = parser.add_subparsers()

        parser_window = subparsers.add_parser('window',
            help='Window command help')
        parser_window.add_argument('--seq', type=str, help='Input sequence')
        parser_window.set_defaults(dest='window')


def add_input_args(parser) -> ArgumentParser:
    return parser
