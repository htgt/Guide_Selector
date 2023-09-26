import os
from typing import List

from tdutils.utils.vcf_utils import Variants

from abstractions.writer import Writer
from mutation_builder import MutationBuilder
from utils.file_system import write_json_failed_guides, write_list_dict_in_tsv, write_variants_to_vcf  # NOQA

GUIDES_CODONS_TSV_FILENAME = 'guides_and_codons.tsv'
VARIANTS_VCF_FILENAME = 'variants.vcf'
FAILED_GUIDES_JSON_FILENAME = 'failed_guides.json'


class MutatorWriter(Writer):
    def __init__(
        self,
        guides_and_codons: List[dict],
        variants: Variants,
        failed_mutations: List[MutationBuilder],
    ) -> None:
        self._guides_and_codons = guides_and_codons
        self._variants = variants
        self._failed_mutations = failed_mutations

    def write_outputs(self, output_dir: str):
        tsv_path = os.path.join(output_dir, GUIDES_CODONS_TSV_FILENAME)
        write_list_dict_in_tsv(tsv_path, self._guides_and_codons)
        print('Output saved to', tsv_path)

        vcf_path = os.path.join(output_dir, VARIANTS_VCF_FILENAME)
        write_variants_to_vcf(vcf_path, self._variants)
        print('Output saved to', vcf_path)

        if self._failed_mutations:
            failed_guides_path = os.path.join(output_dir, FAILED_GUIDES_JSON_FILENAME)
            write_json_failed_guides(failed_guides_path, self._failed_mutations)
            print('Failed guides saved to', failed_guides_path)
