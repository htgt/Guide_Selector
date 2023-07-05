import sys

from utils.arguments_parser import InputArguments
from mutator.mutator import Mutator
from mutator.guide import GuideSequence
from mutator.mutation_builder import get_window_frame
from mutator.data_adapter import build_coding_region_objects
from utils.file_system import read_csv_to_list_dict

def resolve_command(command: str, args: dict) -> None:
    if command == "window":
        guide = GuideSequence(args["seq"], args["strand"], args["window_length"])

        print(guide.window)


def main() -> None:
    parsed_input = InputArguments()
    args = parsed_input.arguments
    command = parsed_input.command

    file_data = read_csv_to_list_dict(file, "\t")
    for row in (file_data):
        cds, window = build_coding_region_objects(row)
        get_window_frame(cds, window)

   # resolve_command(command, args)


if __name__ == '__main__':
    main()
