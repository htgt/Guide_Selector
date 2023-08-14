import sys
from typing import List
from mutator.guide_determiner import GuideDeterminer, parse_gff, write_gff_to_input_tsv
from mutator.runner import Runner
from utils.arguments_parser import InputArguments
from utils.config import prepare_config
from utils.file_system import write_dict_list_to_csv


def resolve_command(command: str, args: dict, config: dict) -> None:
    if command == "mutator":
        run_mutator_cmd(args, config)

    # Temporary for sprint 23. Delete after
    if command == "wge":
        run_wge_cmd(args, config)

def main() -> None:
    parsed_input = InputArguments()
    args = parsed_input.arguments
    config = prepare_config(args['conf'])
    command = parsed_input.command

    resolve_command(command, args, config)


def run_mutator_cmd(args: dict, config: dict) -> None:
    OUTPUT_TSV_FILE = 'output.tsv'
    OUTPUT_VCF_FILE = 'output.vcf'
    runner = Runner(config)

    print('Running PAM & Protospacer mutator')
    # Run Guide Frame Determiner
    guide_determiner = GuideDeterminer()
    guide_data_df = guide_determiner.parse_loci(args['gtf'], args['tsv'])
    runner.parse_coding_regions(guide_data_df)

    # Determine Window and Mutations
    runner.generate_edit_windows_for_builders()
    print("Length of mutation_builders list:", len(runner.mutation_builders))
    print("Length of failed_mutations list:", len(runner.failed_mutations))

    # Write to VCF
    tsv_rows = runner.as_rows(config)
    tsv_path = args['out_dir'] + '/' + OUTPUT_TSV_FILE
    write_dict_list_to_csv(tsv_path, tsv_rows, tsv_rows[0].keys(), "\t")
    print('Output saved to', tsv_path)

    vcf_path = args['out_dir'] + '/' + OUTPUT_VCF_FILE
    runner.write_output_to_vcf(vcf_path)
    print('Output saved to', vcf_path)


# Temporary for sprint 23. Delete after. 
def run_wge_cmd(args: dict, config: dict) -> None:
    gff = ''
    with open('examples/test_guidesX.gff', 'r') as file:
        gff = file.read()

    guide_dicts = parse_gff(gff)
    for entry in guide_dicts:
        print(entry)

    output_file = 'wge.tsv'
    write_gff_to_input_tsv(output_file, guide_dicts)




if __name__ == '__main__':
    main()
