import sys

from dataclasses import dataclass

from utils.arguments_parser import InputArguments
from mutator.mutator import Mutator
from mutator.guide import GuideSequence
from mutator.mutation_builder import get_window_frame
from mutator.data_adapter import build_coding_region_objects
from mutator.base_sequence import BaseSequence
from mutator.edit_window import EditWindow, WindowCodon
from utils.file_system import read_csv_to_list_dict


@dataclass
class Runner:
    cds: BaseSequence
    window: EditWindow
    codon: WindowCodon
    guide: GuideSequence

    def __init__(self):
        self.cds = None
        self.window = None
        self.codon = None
        self.guide = None


    def window_frame(self, input_file_path):
        file_data = read_csv_to_list_dict(input_file_path, "\t")
        for row in (file_data):
            self.cds, self.window = build_coding_region_objects(row)
            get_window_frame(self.cds, self.window)


def resolve_command(command: str, args: dict) -> None:
    runner = Runner()
    if command == "window":
        runner.window_frame(args['file'])


def main() -> None:
    parsed_input = InputArguments()
    args = parsed_input.arguments
    command = parsed_input.command

    resolve_command(command, args)


if __name__ == '__main__':
    main()
