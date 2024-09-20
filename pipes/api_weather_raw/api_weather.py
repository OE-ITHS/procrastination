import requests

def fetch_weather_data() -> None | dict:
    '''
    Fetches current weather data from openweathermap api.

    :returns: :class:`response.json() | None`
        Returns weather data in json format (python dict). Returns None if api request failed.
    :rtype: dict | None
    '''

    api_url = 'https://api.openweathermap.org/data/2.5/weather?lat=59.33&lon=18.06&appid=7e1002f883711d56d3add2b3cab45ba5'

    # Fetch data from weather API.
    response = requests.get(api_url)

    # Check if the fetch returned status_code that indicates success.
    if response.status_code != 200:
        return None
    return response.json()