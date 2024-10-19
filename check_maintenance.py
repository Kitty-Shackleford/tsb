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
        response = requests.get(f'{self.base_url}/maintenance', headers=self._get_headers())
        return response.json()  # Return the JSON response

if __name__ == "__main__":
    api = NitradoAPI(os.environ['NITRADO_TOKEN'])
    maintenance_data = api.check_maintenance()
    
    if maintenance_data['status'] == 'success':
        print("Maintenance Status:")
        for backend, status in maintenance_data['data']['maintenance'].items():
            print(f"{backend}: {'Operational' if not status else 'Under Maintenance'}")
    else:
        print("Failed to retrieve maintenance status.")

