import sys

from mutator.guide_determiner import GuideDeterminer
from mutator.runner import Runner, mutator_to_dict_list
from utils.arguments_parser import InputArguments
from utils.file_system import read_csv_to_list_dict, write_dict_list_to_csv
from pprint import pprint

OUTFUT_FILE_HEADERS = [
    'guide_id',
    'chromosome',
    'cds_strand',
    'gene_name',
    'guide_strand',
    'guide_start',
    'guide_end',
    'window_pos',
    'pos',
    'ref_codon',
    'ref_pos_three'
]


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

    tsv_rows = runner.as_rows()
    print('Output saved to', OUTPUT_FILE_URL)


    # Determine Window
    print("Length of mutation_builders list:", len(runner.mutation_builders))

    runner.generate_edit_windows_for_builders()
    print("Length of mutation_builders list:", len(runner.mutation_builders))
    print("Length of failed_mutations list:", len(runner.failed_mutations))


    # 3rd Base finder
    # Mutation finder
    # Filter mutators
    # Write to VCF


if __name__ == '__main__':
    main()
