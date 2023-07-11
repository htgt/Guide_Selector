import sys

from mutator.runner import Runner, mutator_to_dict_list
from utils.arguments_parser import InputArguments
from utils.file_system import read_csv_to_list_dict, write_dict_list_to_csv


def resolve_command(command: str, args: dict) -> None:
    if command == "window":
        run_window_cmd(args)

def main() -> None:
    parsed_input = InputArguments()
    args = parsed_input.arguments
    command = parsed_input.command

    resolve_command(command, args)

def run_window_cmd(args : dict) -> None:
    OUTPUT_FILE_URL = 'output.tsv'
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

    rows = []
    file_data = read_csv_to_list_dict(args['file'], "\t")
    for row in (file_data):
        runner = Runner()
        runner.run_window_frame(row)
        rows.append(runner)

    dict_list = mutator_to_dict_list(rows)

    write_dict_list_to_csv(OUTPUT_FILE_URL, dict_list, OUTFUT_FILE_HEADERS, '\t')

    print('Window command success')
    print('Output saved to', OUTPUT_FILE_URL)


if __name__ == '__main__':
    main()
