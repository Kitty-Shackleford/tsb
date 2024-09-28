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
        return response

    def check_services(self):
        response = requests.get(f'{self.base_url}/services', headers=self._get_headers())
        return response


def main():
    api_key = os.getenv('NITRADO_TOKEN')
    nitrado_api = NitradoAPI(api_key)

    maintenance_summary = "# Nitrado Maintenance Status\n\n"
    services_summary = "# Nitrado Services Status\n\n"

    # Check Maintenance Status
    maintenance_response = nitrado_api.check_maintenance()
    if maintenance_response.status_code == 200:
        maintenance_data = maintenance_response.json().get('data', {}).get('maintenance', {})
        maintenance_summary += "### Maintenance Status:\n"
        for key, value in maintenance_data.items():
            maintenance_summary += f"- **{key.replace('_', ' ').capitalize()}**: {'Yes' if value else 'No'}\n"
    else:
        maintenance_summary += f"Failed to retrieve maintenance status. Status Code: {maintenance_response.status_code}\n"

    # Check Services Status
    services_response = nitrado_api.check_services()
    if services_response.status_code == 200:
        services = services_response.json().get('data', {}).get('services', [])
        for service in services:
            services_summary += f"- **Service ID**: {service['id']}\n"
            services_summary += f"  - **Status**: {service['status']}\n"
            services_summary += f"  - **Game**: {service['details']['game']}\n\n"
    else:
        services_summary += f"Failed to retrieve services. Status Code: {services_response.status_code}\n"

    # Combine summaries
    full_summary = f"{maintenance_summary}\n\n{services_summary}"
    print(full_summary)

if __name__ == "__main__":
    main()
