from argparse import ArgumentParser, _SubParsersAction


class InputArguments:
    def __init__(self) -> None:
        self.arguments = {}
        self.command = ''

        self.parse_arguments()

    def set_args(self, values) -> None:
        self.arguments = values
        self.command = values['command']

    def parse_arguments(self) -> dict:
        parser = ArgumentParser(
            description='Guide Selection CLI',
            prog='Guide Selection'
        )

        self._add_subparsers(parser)

        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s 0.0.1'
        )


        parser = add_input_args(parser)

        self.set_args(vars(parser.parse_args()))

    def _add_subparsers(self, parser) -> None:
        subparsers = parser.add_subparsers(dest='command')

        self._add_mutator_command_parser(subparsers)
        self._add_retrieve_command_parser(subparsers)

    def _add_mutator_command_parser(self, subparsers: _SubParsersAction) -> None:
        parser_mutator = subparsers.add_parser('mutator', help='Mutator command help')
        parser_mutator.add_argument('--tsv', type=str,
            help='Path to Guide Locus as TSV file. Required columns: guide start, end, strand and id')
        parser_mutator.add_argument('--gtf', type=str, help='Path to reference GTF file')
        parser_mutator.add_argument(
            '--conf',
            type=str,
            help='Path to custom configuration file',
            default='',
        )
        parser_mutator.add_argument(
            '--out_dir',
            type=str,
            nargs='?',
            const='.',
            default='./',
            help='Desired output path (Default: ./)'
        )

    def _add_retrieve_command_parser(self, subparsers: _SubParsersAction) -> None:
        parser_retrieve = subparsers.add_parser('retrieve', help='Retrieve command help')


def add_input_args(parser) -> ArgumentParser:
    return parser
