import os

from typing import List

from mutator.guide import GuideSequence
from mutator.guide_determiner import GuideDeterminer
from mutator.runner import Runner
from mutator.retrieve import get_target_regions, get_guides_data
from utils.file_system import write_json_failed_guides
from utils.arguments_parser import InputArguments
from utils.config import prepare_config
from utils.file_system import write_dict_list_to_csv, read_gtf_to_df
from adaptors.parsers.parse_guide_tsv import read_guide_tsv_to_guide_sequences
from adaptors.parsers.parse_wge_gff import read_wge_gff_to_guide_sequences
from adaptors.serialisers.serialise_guide_sequences import write_guide_sequences_to_tsv


def resolve_command(command: str, args: dict, config: dict) -> None:
    if command == "mutator":
        run_mutator_cmd(args, config)
    if command == "retrieve":
        run_retrieve_cmd(args, config)

def main() -> None:
    parsed_input = InputArguments()
    args = parsed_input.arguments
    config = prepare_config(args['conf'])
    command = parsed_input.command

    resolve_command(command, args, config)


def run_guide_selector_cmd(args: dict, config: dict) -> None:
    guide_sequences = run_retrieve_cmd(args, config)

    run_mutator_cmd(args, config, guide_sequences)


def run_retrieve_cmd(args: dict, config: dict) -> List[GuideSequence]:
    OUTPUT_FILE = 'guides.tsv'

    regions = get_target_regions(region=args['region'], region_file=args['region_file'])

    request_options = {
        'species_id': config['species_id'],
        'assembly': config['assembly']

    }
    guide_sequences = get_guides_data(regions, request_options)

    output_path = os.path.join(args['out_dir'], OUTPUT_FILE)
    write_guide_sequences_to_tsv(output_path, guide_sequences)

    print('====================================')
    print('Guides retrieved: ', len(guide_sequences))
    print('Output saved to: ', output_path)

    return guide_sequences


def run_mutator_cmd(args: dict, config: dict, guide_sequences: List[GuideSequence] = None) -> None:
    OUTPUT_TSV_FILE = 'output.tsv'
    OUTPUT_VCF_FILE = 'output.vcf'
    runner = Runner(config)

    print('Running PAM & Protospacer mutator')
    # Run Guide Frame Determiner
    gtf_data = read_gtf_to_df(args['gtf'])
    if not guide_sequences:
        guide_sequences = read_guide_tsv_to_guide_sequences(args['tsv'])
    guide_determiner = GuideDeterminer()
    guide_data_df = guide_determiner.parse_loci(gtf_data, guide_sequences)

    runner.create_mutation_builders(guide_data_df)

    # Determine Window
    print("Length of mutation_builders list:", len(runner.mutation_builders))

    runner.generate_edit_windows_for_builders()
    print("Length of mutation_builders list:", len(runner.mutation_builders))
    print("Length of failed_mutations list:", len(runner.failed_mutations))

    # Write Output Files
    tsv_rows = runner.as_rows(config)
    tsv_path = os.path.join(args['out_dir'], OUTPUT_TSV_FILE)

    write_dict_list_to_csv(tsv_path, tsv_rows, tsv_rows[0].keys(), "\t")
    print('Output saved to', tsv_path)

    vcf_path = os.path.join(args['out_dir'], 'output.vcf')
    runner.write_output_to_vcf(vcf_path)
    print('Output saved to', vcf_path)

    if runner.failed_mutations:
        failed_guides_path = os.path.join(args['out_dir'], 'failed_guides.json')
        write_json_failed_guides(failed_guides_path, runner.failed_mutations)
        print('Failed guides saved to', failed_guides_path)


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
