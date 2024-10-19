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

    def check_services(self):
        response = requests.get(f'{self.base_url}/services', headers=self._get_headers())
        return response

def main():
    api_key = os.getenv('NITRADO_TOKEN')
    nitrado_api = NitradoAPI(api_key)
    
    response = nitrado_api.check_services()
    
    if response.status_code == 200:
        services = response.json().get('data', {}).get('services', [])
        for service in services:
            print(f"Service ID: {service['id']}, Status: {service['status']}, Game: {service['details']['game']}")
    else:
        print(f"Failed to retrieve services. Status Code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    main()
