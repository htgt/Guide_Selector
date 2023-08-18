import requests

def get_data_from_wge_by_coords(
        chromosome: str,
        start: int,
        end: int,
        species_id: str='GRCh38',
        assembly: str='GRCh38'
):
    base_url = "https://wge.stemcell.sanger.ac.uk/api/crisprs_in_region"
    url = f"{base_url}?chr={chromosome}&start={start}&end={end}&species_id={assembly}&assembly={assembly}"

    headers = {'Content-type': 'text/plain'}
    response = requests.get(url, headers=headers)

    if response.status_code == requests.codes.ok:
        return response.text
    else:
        raise requests.exceptions.RequestException

