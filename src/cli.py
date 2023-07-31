import sys

from mutator.guide_determiner import GuideDeterminer
from mutator.runner import Runner, mutator_to_dict_list
from utils.arguments_parser import InputArguments
from utils.file_system import read_csv_to_list_dict, write_dict_list_to_csv
from pprint import pprint


def resolve_command(command: str, args: dict) -> None:
    if command == "mutator":
        run_mutator_cmd(args)

def main() -> None:
    parsed_input = InputArguments()
    args = parsed_input.arguments
    command = parsed_input.command

    resolve_command(command, args)

def run_mutator_cmd(args : dict) -> None:
    OUTPUT_FILE_URL = 'output.tsv'

    runner = Runner()
    print('Running PAM mutator')
    # Run Guide Frame Determiner
    guide_determiner = GuideDeterminer()
    guide_data_df = guide_determiner.parse_loci(args['gtf'], args['tsv'])
    runner.parse_coding_regions(guide_data_df)

    # Determine Window
    print("Length of mutation_builders list:", len(runner.mutation_builders))

    runner.generate_edit_windows_for_builders()
    print("Length of mutation_builders list:", len(runner.mutation_builders))
    print("Length of failed_mutations list:", len(runner.failed_mutations))


    tsv_rows = runner.as_rows(guide_determiner.prepare_config(args['conf']))
    tsv_path = args['out'] + '/' + OUTPUT_FILE_URL
    write_dict_list_to_csv(tsv_path, tsv_rows, tsv_rows[0].keys(), "\t")
    print('Output saved to', tsv_path)


    # 3rd Base finder
    # Mutation finder
    # Filter mutators
    # Write to VCF


if __name__ == '__main__':
    main()
