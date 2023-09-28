import os
from typing import List

from tdutils.utils.vcf_utils import Variants

from abstractions.writer import Writer
from mutation_builder import MutationBuilder
from utils.file_system import write_json_failed_guides, write_list_dict_in_tsv, write_variants_to_vcf  # NOQA


class MutatorWriter(Writer):
<<<<<<< Updated upstream
=======
    guides_codons_tsv_filename = 'guides_and_codons.tsv'
    variants_vcf_filename = 'variants.vcf'
    failed_guides_json_filename = 'failed_guides.json'

>>>>>>> Stashed changes
    def __init__(
        self,
        guides_and_codons: List[dict],
        variants: Variants,
        failed_mutations: List[MutationBuilder],
    ) -> None:
        self._kept_guides = kept_guides
        self._discarded_guides = discarded_guides
        self._variants = variants
        self._failed_guides = failed_guides

    def write_outputs(self, output_dir: str):
<<<<<<< HEAD
        self._write_tsv_guide_and_codons_file(output_dir)

        if self._discarded_guides:
            self._write_tsv_discarded_guides_and_codons_file(output_dir)

        self._write_vcf_variants_file(output_dir)

        if self._failed_guides:
            self._write_json_failed_guides_file(output_dir)

    def _write_tsv_guide_and_codons_file(self, output_dir):
        tsv_path = os.path.join(output_dir, MutatorWriter.guides_codons_tsv_filename)
        write_list_dict_in_tsv(tsv_path, self._kept_guides)
        print('Output saved to', tsv_path)

    def _write_tsv_discarded_guides_and_codons_file(self, output_dir):
        tsv_path = os.path.join(output_dir, MutatorWriter.discarded_guides_codons_tsv_filename)
        write_list_dict_in_tsv(tsv_path, self._discarded_guides)
        print('Output saved to', tsv_path)

    def _write_vcf_variants_file(self, output_dir):
=======
        tsv_path = os.path.join(output_dir, MutatorWriter.guides_codons_tsv_filename)
        write_list_dict_in_tsv(tsv_path, self._guides_and_codons)
        print('Output saved to', tsv_path)

>>>>>>> fb8c165... TD-459fomatted code style
        vcf_path = os.path.join(output_dir, MutatorWriter.variants_vcf_filename)
        write_variants_to_vcf(vcf_path, self._variants)
        print('Output saved to', vcf_path)

<<<<<<< HEAD
    def _write_json_failed_guides_file(self, output_dir):
        failed_guides_path = os.path.join(output_dir, MutatorWriter.failed_guides_json_filename)
        write_json_failed_guides(failed_guides_path, self._failed_guides)
        print('Failed guides saved to', failed_guides_path)
=======
        if self._failed_mutations:
            failed_guides_path = os.path.join(output_dir, MutatorWriter.failed_guides_json_filename)
            write_json_failed_guides(failed_guides_path, self._failed_mutations)
            print('Failed guides saved to', failed_guides_path)
>>>>>>> fb8c165... TD-459fomatted code style
