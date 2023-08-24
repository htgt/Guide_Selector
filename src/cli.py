import sys
import os.path

from typing import List
from mutator.guide_determiner import GuideDeterminer
from mutator.runner import Runner
from mutator.retrieve import \
    retrieve_data_for_region, \
    get_target_regions, \
    get_regions_data, \
    get_guides_data, \
    write_gff_to_input_tsv
from utils.file_system import write_json_failed_guides
from utils.arguments_parser import InputArguments
from utils.config import prepare_config
from utils.file_system import write_dict_list_to_csv


def resolve_command(command: str, args: dict, config: dict) -> None:
    if command == "mutator":
        run_mutator_cmd(args, config)
    if command == "retrieve":
        run_retrieve_cmd(args, config)
    if command == "guide_selector":
        run_guide_selector_cmd(args, config)



def main() -> None:
    parsed_input = InputArguments()
    args = parsed_input.arguments
    config = prepare_config(args['conf'])
    command = parsed_input.command

    resolve_command(command, args, config)


def run_guide_selector_cmd(args: dict, config: dict) -> None:
    tsv_path = run_retrieve_cmd(args, config)

    args["tsv"] = tsv_path
    run_mutator_cmd(args, config)


def run_retrieve_cmd(args: dict, config: dict) -> str:
    OUTPUT_FILE = 'guides.tsv'
    print('Run retrieve command with config:', config)

    regions = get_target_regions(args)

    guide_dicts = get_guides_data(regions, config)

    output_path = os.path.join(args['out_dir'], OUTPUT_FILE)
    write_gff_to_input_tsv(output_path, guide_dicts)

    print('====================================')
    print('Guides retrieved: ', len(guide_dicts))
    print('Output saved to: ', output_path)

    return output_path


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

    # Write Output Files
    tsv_rows = runner.as_rows(config)
    tsv_path = os.path.join(args['out_dir'], OUTPUT_TSV_FILE)
    write_dict_list_to_csv(tsv_path, tsv_rows, tsv_rows[0].keys(), "\t")
    print('Output saved to', tsv_path)

    vcf_path = os.path.join(args['out_dir'], OUTPUT_VCF_FILE)
    runner.write_output_to_vcf(vcf_path)
    print('Output saved to', vcf_path)

    if runner.failed_mutations:
        failed_guides_path = os.path.join(args['out_dir'], 'failed_guides.json')
        write_json_failed_guides(failed_guides_path, runner.failed_mutations)
        print('Failed guides saved to', failed_guides_path)


if __name__ == '__main__':
    main()
