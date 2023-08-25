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

        self._add_input_args(parser)
        self._add_subparsers(parser)

        self.set_args(vars(parser.parse_args()))

    @staticmethod
    def _add_input_args(parser) -> None:
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s 0.0.1',
        )
        parser.add_argument(
            '--conf',
            type=str,
            help='Path to custom configuration file',
            default='',
        )
        parser.add_argument(
            '--out_dir',
            type=str,
            nargs='?',
            const='.',
            default='./',
            help='Desired output path (Default: ./)',
        )

    def _add_subparsers(self, parser) -> None:
        subparsers = parser.add_subparsers(dest='command')

        self._add_mutator_command_parser(subparsers)
        self._add_retrieve_command_parser(subparsers)
        self._add_guide_selector_command_parser(subparsers)

    @staticmethod
    def _add_mutator_command_parser(subparsers: _SubParsersAction) -> None:
        parser_mutator = subparsers.add_parser('mutator', help='Mutator command help')
        parser_mutator.add_argument(
            '--tsv',
            type=str,
            help='Path to Guide Locus as TSV file. Required columns: guide start, end, strand and id'
        )
        parser_mutator.add_argument(
            '--gtf',
            type=str,
            help='Path to reference GTF file'
        )

    def _add_guide_selector_command_parser(self, subparsers: _SubParsersAction) -> None:
        parser_guide_selector = subparsers.add_parser(
            'guide_selector',
            help='Guide Selector command to run retrieve->mutator together'
        )

        self._add_region_group(parser_guide_selector)

        parser_guide_selector.add_argument(
            '--gtf',
            type=str,
            help='Path to reference GTF file'
        )

    def _add_retrieve_command_parser(self, subparsers: _SubParsersAction) -> None:
        parser_retrieve = subparsers.add_parser('retrieve', help='Retrieve command help')
        self._add_region_group(parser_retrieve)

    @staticmethod
    def _add_region_group(parser: ArgumentParser):
        region_group = parser.add_mutually_exclusive_group()

        region_group.add_argument(
            '--region',
            type=str,
            help='Target region specified in format chr1:1-10001'
        )
        region_group.add_argument(
            '--region_file',
            type=str,
            help='Path to the input file with data for Target Regions separated by new line'
        )

