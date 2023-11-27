from typing import List

from config.config import Config
from guide import GuideSequence
from mutator.mutator import Mutator
from retriever.retriever import Retriever
from utils.arguments_parser import InputArguments


def main() -> None:
    parsed_input = InputArguments()
    args = parsed_input.arguments
    config = Config(args['conf'], args)
    command = parsed_input.command

    resolve_command(command, config)


def resolve_command(command: str, config: Config) -> None:
    if command == "mutator":
        run_mutator_cmd(config)
    if command == "retrieve":
        run_retrieve_cmd(config)
    if command == "guide_selector":
        run_guide_selector_cmd(config)


def run_guide_selector_cmd(config: Config) -> None:
    guide_sequences = run_retrieve_cmd(config)

    run_mutator_cmd(config, guide_sequences)


def run_retrieve_cmd(config: Config) -> List[GuideSequence]:
    retriever = Retriever(config.config_dict)
    print('Run retrieve command with config:', config)

    # Read Input Files
    retriever.read_inputs(config.args)

    # Run retriever
    retriever.run()

    # Write Output Files
    retriever.write_outputs(output_dir=config.args['out_dir'])

    return retriever.guide_sequences


def run_mutator_cmd(config: Config, guide_sequences: List[GuideSequence] = None) -> None:
    mutator = Mutator(config.config_dict)
    print('Running PAM & Protospacer guide_selector')

    # Read Input Files
    mutator.read_inputs(config.args, guide_sequences)

    # Run mutator
    mutator.run()
    print("Length of mutation_builders list:", len(mutator.mutation_builders))
    print("Length of failed_mutations list:", len(mutator.failed_mutations))

    # Write Output Files
    mutator.write_outputs(output_dir=config.args['out_dir'])


if __name__ == '__main__':
    main()
