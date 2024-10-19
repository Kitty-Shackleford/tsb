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

    def health_check(self):
        response = requests.get(f'{self.base_url}/services', headers=self._get_headers())
        return response  # Return the full response object for inspection

if __name__ == "__main__":
    api = NitradoAPI(os.environ['API_KEY'])
    response = api.health_check()

    if response.status_code == 200:
        health_data = response.json()
        print(f"API Status: {health_data.get('status', 'Unknown status')}")
        print(f"Message: {health_data.get('message', 'No message available')}")
    else:
        print('API Health Check Failed!')
        print(f'Status Code: {response.status_code}')
        print(f'Response Content: {response.text}')
