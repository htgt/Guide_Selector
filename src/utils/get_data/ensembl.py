import requests

def get_seq_from_ensembl_by_coords(start, end):
    url = 'https://rest.ensembl.org/sequence/region/human/X:67626572..67626594:1'
    headers = {'Content-type':'text/plain'}
    response = requests.get(url, headers=headers)

    if response.codes.ok:
        return response.text
    else:
        raise requests.exceptions.RequestException

    