import sys

from mutator.runner import Runner
from utils.arguments_parser import InputArguments
from utils.file_system import read_csv_to_list_dict


def resolve_command(command: str, args: dict) -> None:
    rows = []
    if command == "window":
        file_data = read_csv_to_list_dict(args['file'], "\t")
        for row in (file_data):
            runner = Runner()
            rows.append(runner.window_frame(row))


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
