import requests

# Configuration
PORT_API_BASE_URL = "https://api.getport.io/v1"
CLIENT_ID = "w21elwSTA20k4IDRpkBHiZQ0LreluWpi"
CLIENT_SECRET = "1IausB3T1HuLKLa2wfWakfxyZykswKWuZpKHvE9K1Cca9d0NuWKft8LJZmysJHZp"
TOKEN_URL = f"{PORT_API_BASE_URL}/oauth2/token"

def get_access_token(client_id, client_secret):
    response = requests.post(TOKEN_URL, data={
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    })
    response.raise_for_status()
    return response.json()['accessToken']

def get_service_entities(headers):
    url = f"{PORT_API_BASE_URL}/service-entities"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_eol_packages_for_service(service_id, headers):
    url = f"{PORT_API_BASE_URL}/service-entities/{service_id}/frameworks"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    frameworks = response.json()
    eol_packages_count = sum(1 for framework in frameworks if framework.get('eol', False))
    return eol_packages_count

def update_service_entity(service_id, eol_packages_count, headers):
    url = f"{PORT_API_BASE_URL}/service-entities/{service_id}"
    data = {
        "properties": {
            "eol_packages_count": eol_packages_count
        }
    }
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def main():
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    service_entities = get_service_entities(headers)
    for service in service_entities:
        service_id = service['id']
        eol_packages_count = get_eol_packages_for_service(service_id, headers)
        update_response = update_service_entity(service_id, eol_packages_count, headers)
        print(f"Updated service {service_id} with {eol_packages_count} EOL packages.")

if __name__ == "__main__":
    main()