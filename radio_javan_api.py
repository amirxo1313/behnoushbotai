# radio_javan_api.py
import requests
from config import RADIO_JAVAN_ACCESS_KEY

class RadioJavanAPI:
    API_URL = "https://api.ineo-team.ir/rj.php"

    def __init__(self, access_key):
        self.access_key = access_key

    def request(self, action, params=None):
        if params is None:
            params = {}
        params['accessKey'] = self.access_key
        params['action'] = action
        response = requests.post(self.API_URL, data=params)
        return response.json()

    def search(self, query):
        """Search for music or media."""
        return self.request("search", {'query': query})
