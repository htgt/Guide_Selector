import sys

from mutator.runner import Runner, write_mutator_to_tsv
from utils.arguments_parser import InputArguments
from utils.file_system import read_csv_to_list_dict
from utils.file_system import write_dict_list_to_tsv


def resolve_command(command: str, args: dict) -> None:
    if command == "window":
        run_window_cmd(args)

def main() -> None:
    parsed_input = InputArguments()
    args = parsed_input.arguments
    command = parsed_input.command

    file_data = read_csv_to_list_dict(file, "\t")
    for row in (file_data):
        cds, window = build_coding_region_objects(row)
        get_window_frame(cds, window)

   # resolve_command(command, args)

def run_window_cmd(args : dict) -> None:
    rows = []
    file_data = read_csv_to_list_dict(args['file'], "\t")
    for row in (file_data):
        runner = Runner()
        rows.append(runner.window_frame(row))

    dict_list = write_mutator_to_tsv(rows)
    headers = [
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
    write_dict_list_to_csv('output.tsv', dict_list, headers, '\t')


if __name__ == '__main__':
    main()
