import os
from typing import List

import pandas as pd
from tdutils.utils.vcf_utils import Variants

from abstractions.writer import Writer
from mutation_builder import MutationBuilder
from utils.file_system import write_json_failed_guides, write_list_dict_in_tsv, write_variants_to_vcf  # NOQA


class MutatorWriter(Writer):
    guides_codons_tsv_filename = 'candidate_ppes.tsv'
    discarded_guides_codons_tsv_filename = 'discarded_ppes.tsv'
    variants_vcf_filename = 'candidate_ppes.vcf'
    failed_guides_json_filename = 'failed_guides.json'
    ranked_guides_tsv_filename = 'ranked_guides.tsv'
    best_guide_variants = 'optimal_guide_ppes.vcf'

    def __init__(
        self,
        guides_and_codons: List[dict],
        variants: Variants,
        failed_guides: List[MutationBuilder],
        ranked_guides_df: pd.DataFrame,
    ) -> None:
        self._kept_guides = kept_guides
        self._discarded_guides = discarded_guides
        self._variants = variants
        self._failed_guides = failed_guides
        self._ranked_guides_df = ranked_guides_df

    def write_outputs(self, output_dir: str):
        self._write_tsv_guide_and_codons_file(output_dir)

        if self._discarded_guides:
            self._write_tsv_discarded_guides_and_codons_file(output_dir)

        self._write_vcf_variants_file(output_dir, MutatorWriter.variants_vcf_filename)

        if self._failed_guides:
            self._write_json_failed_guides_file(output_dir)

        self._write_tsv_ranked_guides(output_dir)

    def _write_tsv_guide_and_codons_file(self, output_dir):
        tsv_path = os.path.join(output_dir, MutatorWriter.guides_codons_tsv_filename)
        if self._kept_guides:
            write_list_dict_in_tsv(tsv_path, self._kept_guides)
            print('Output saved to', tsv_path)
        else:
            print('No guides persisted to ', MutatorWriter.guides_codons_tsv_filename)

    def _write_tsv_discarded_guides_and_codons_file(self, output_dir):
        tsv_path = os.path.join(output_dir, MutatorWriter.discarded_guides_codons_tsv_filename)
        write_list_dict_in_tsv(tsv_path, self._discarded_guides)
        print('Output saved to', tsv_path)

    def _write_vcf_variants_file(self, output_dir, variants: Variants = None):
        if not variants:
            variants = self._variants

        vcf_path = os.path.join(output_dir, MutatorWriter.variants_vcf_filename)
        write_variants_to_vcf(vcf_path, variants)
        print('Output saved to', vcf_path)

    def _write_json_failed_guides_file(self, output_dir):
        failed_guides_path = os.path.join(output_dir, MutatorWriter.failed_guides_json_filename)
        write_json_failed_guides(failed_guides_path, self._failed_guides)
        print('Failed guides saved to', failed_guides_path)

    def _write_tsv_ranked_guides(self, output_dir):
        ranked_guides_path = os.path.join(output_dir, MutatorWriter.ranked_guides_tsv_filename)

        self._ranked_guides_df.to_csv(ranked_guides_path, index_label='ranking')

        print('Ranked guides saved to ', ranked_guides_path)
