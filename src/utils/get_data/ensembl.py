import requests

def get_seq_from_ensembl_by_coords(chromosome:str, start:int, end:int):
    url = 'https://rest.ensembl.org/sequence/region/human/' + chromosome + ':' + str(start) + '..' + str(end) + ':1'
    headers = {'Content-type':'text/plain'}
    response = requests.get(url, headers=headers)

    if response.status_code == requests.codes.ok:
        return response.text
    else:
        raise requests.exceptions.RequestException

    