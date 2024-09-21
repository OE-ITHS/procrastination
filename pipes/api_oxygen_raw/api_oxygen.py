import requests

def fetch_oxygen_data() -> None | dict:
    '''
    Fetches current oxygen data from SMHI's api.

    :returns: :class:`response.json() | None`
        Returns oxygen data in json format (python dict). Returns None if api request failed.
    :rtype: dict | None
    '''

    api_url = 'https://opendata-download-ocobs.smhi.se/api/version/latest/parameter/15/station/33002/period/latest-hour/data.json'

    # Fetch data from SMHI oxygen API.
    response = requests.get(api_url)

    response_json = {key:response.json()[key] for key in ['updated', 'parameter', 'station', 'period', 'position']}

    response_json['value_d1'] = next((item for item in response.json()['value'] if item['depth'] == '1'), None)
    response_json['value_d5'] = next((item for item in response.json()['value'] if item['depth'] == '5'), None)

    # Check if the fetch returned status_code that indicates success.
    if response.status_code != 200:
        return None
    return response_json