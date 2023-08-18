from typing import List
import gffutils
from utils.file_system import read_csv_to_list_dict, write_dict_list_to_csv
from utils.get_data.wge import get_data_from_wge_by_coords
from mutator.target_region import parse_string_to_target_region, TargetRegion
from utils.exceptions import GetDataFromWGEError


def get_regions_data(args: dict) -> List[str]:
    if args['region']:
        return [{"region": args['region']}]
    else:
        if args['file']:
            return read_csv_to_list_dict(args['file'], delimiter="\t")
        else:
            raise ValueError('No input data for Target Regions')


def get_guides_data(regions: List[str], config: dict) -> List[dict]:
    guide_dicts = []
    for line in regions:
        print('Retrieve data for Target Region',
              line["id"] if "id" in line else "")

        try:
            data = retrieve_data_for_region(line["region"], config)
            guide_dicts.extend(data)

        except GetDataFromWGEError:
            pass

    return guide_dicts


def retrieve_data_for_region(region_string: str, config: dict) -> dict:
    region = parse_string_to_target_region(region_string)

    gff_data = get_data_from_wge_by_coords(
        chromosome=region.chromosome,
        start=region.start,
        end=region.end,
        species_id=config['species_id'],
        assembly=config['assembly'],
    )

    try:
        guide_dicts = parse_gff(gff_data)
        return guide_dicts

    except Exception:
        print(f'No data from WGE for given region: {region_string}')
        raise GetDataFromWGEError()


def parse_gff(gff_data: dict):
    db = gffutils.create_db(data=gff_data, dbfn=':memory:', from_string=True)
    entries = []

    for feature in db.features_of_type('Crispr'):
        chromosome = 'chr' + feature.seqid.strip()
        entry = {
            'guide_id' : feature.attributes['Name'][0],
            'chr' : chromosome,
            'start' : int(feature.start),
            'end' : int(feature.end),
            'grna_strand' : feature.strand,
            'ot_summary' : feature.attributes['Name'][0],
            'seq': feature.attributes['CopySequence'][0],
        }

        entries.append(entry)

    return entries


def write_gff_to_input_tsv(file : str, gff : List[dict]) -> None:
    headers = ['guide_id', 'chr', 'start', 'end', 'grna_strand']

    tsv_rows = []
    for entry in gff:
        entry_copy = entry.copy()
        del entry_copy['ot_summary']
        del entry_copy['seq']
        tsv_rows.append(entry_copy)

    write_dict_list_to_csv(file, tsv_rows, headers, "\t")
    print(f'Data written to {file}')
