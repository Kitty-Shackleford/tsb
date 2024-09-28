import requests
import os

class NitradoAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.nitrado.net'

    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def check_maintenance(self):
        response = requests.get(f'{self.base_url}/services', headers=self._get_headers())
        if response.status_code == 200:
            maintenance_data = response.json().get('data', {}).get('maintenance', {})
            return maintenance_data
        else:
            print(f'Error: Received status code {response.status_code}')
            print(f'Response content: {response.text}')
            return None

if __name__ == "__main__":
    api = NitradoAPI(os.environ['NITRADO_TOKEN'])
    maintenance_status = api.check_maintenance()

    if maintenance_status is not None:
        print('Maintenance Status:')
        for key, value in maintenance_status.items():
            print(f'{key}: {value}')
    else:
        print('Failed to retrieve maintenance status.')
