import sys

from mutator.guide_determiner import GuideDeterminer
from mutator.runner import Runner, mutator_to_dict_list
from utils.arguments_parser import InputArguments
from utils.file_system import read_csv_to_list_dict, write_dict_list_to_csv


def resolve_command(command: str, args: dict) -> None:
    if command == "mutator":
        run_mutator_cmd(args)

def main() -> None:
    parsed_input = InputArguments()
    args = parsed_input.arguments
    command = parsed_input.command

    resolve_command(command, args)

def run_mutator_cmd(args : dict) -> None:
    runner = Runner()
    print('Running PAM mutator')
    # Run Guide Frame Determiner
    guide_determiner = GuideDeterminer()
    guide_data_df = guide_determiner.parse_loci(args['gtf'], args['tsv'])
    runner.parse_coding_regions(guide_data_df)
    # Determine Window
    # 3rd Base finder
    # Mutation finder
    # Filter mutators
    # Write to VCF


if __name__ == '__main__':
    main()
