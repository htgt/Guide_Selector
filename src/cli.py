from typing import List

from guide import GuideSequence
from mutator.mutator import Mutator
from retriever.retriever import Retriever
from utils.arguments_parser import InputArguments
from utils.config import prepare_config


def main() -> None:
    parsed_input = InputArguments()
    args = parsed_input.arguments
    config = prepare_config(args['conf'])
    command = parsed_input.command

    resolve_command(command, args, config)


def resolve_command(command: str, args: dict, config: dict) -> None:
    if command == "mutator":
        run_mutator_cmd(args, config)
    if command == "retrieve":
        run_retrieve_cmd(args, config)
    if command == "guide_selector":
        run_guide_selector_cmd(args, config)


def run_guide_selector_cmd(args: dict, config: dict) -> None:
    guide_sequences = run_retrieve_cmd(args, config)

    run_mutator_cmd(args, config, guide_sequences)


def run_retrieve_cmd(args: dict, config: dict) -> List[GuideSequence]:
    retriever = Retriever(config)
    print('Run retrieve command with config:', config)

    # Read Input Files
    retriever.read_inputs(args)

    # Run retriever
    retriever.run()

    # Write Output Files
    retriever.write_outputs(output_dir=args['out_dir'])

    return retriever.guide_sequences


def run_mutator_cmd(args: dict, config: dict, guide_sequences: List[GuideSequence] = None) -> None:
    mutator = Mutator(config)
    print('Running PAM & Protospacer guide_selector')

    # Read Input Files
    mutator.read_inputs(args, guide_sequences)

    # Run mutator
    mutator.run()
    print("Length of mutation_builders list:", len(mutator.mutation_builders))
    print("Length of failed_mutations list:", len(mutator.failed_mutations))

    # Write Output Files
    mutator.write_outputs(output_dir=args['out_dir'])

    # Ranking output
    print('rank')
    mutator_df = mutator.convert_to_dataframe()
    print(mutator_df)

if __name__ == '__main__':
    main()
