import requests

from config import *

headers_client = {
    "Authorization": f"Bearer {CLIENT_KEY_PTERO}",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "CF-Access-Client-Id": f"{CF_CLIENT_ID}",
    "CF-Access-Client-Secret": f"{CF_CLIENT_SECRET}",
}

headers_application = {
    "Authorization": f"Bearer {APP_KEY_PTERO}",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "CF-Access-Client-Id": f"{CF_CLIENT_ID}",
    "CF-Access-Client-Secret": f"{CF_CLIENT_SECRET}",
    "cookie": "pterodactyl_session=eyJpdiI6InhIVXp5ZE43WlMxUU1NQ1pyNWRFa1E9PSIsInZhbHVlIjoiQTNpcE9JV3FlcmZ6Ym9vS0dBTmxXMGtST2xyTFJvVEM5NWVWbVFJSnV6S1dwcTVGWHBhZzdjMHpkN0RNdDVkQiIsIm1hYyI6IjAxYTI5NDY1OWMzNDJlZWU2OTc3ZDYxYzIyMzlhZTFiYWY1ZjgwMjAwZjY3MDU4ZDYwMzhjOTRmYjMzNDliN2YifQ%253D%253D"
}

servers = {}


async def get_server_status(server):
    response = requests.request('GET', f'{BASE_URL}api/client/servers/{server}/resources', headers=headers_client)
    data = response.json()
    state = data['attributes']['current_state']
    if state == "running":
        return "ONLINE"
    else:
        return state.upper()


def get_servers():
    response = requests.request('GET', f'{BASE_URL}api/application/servers', headers=headers_application)
    data = response.json()
    for f in data['data']:
        server_name = f['attributes']['name']
        server_uuid = f['attributes']['identifier']
        servers.update({server_name: server_uuid})
    return servers


async def change_power_state(server, state):
    payload = '{"signal": "%s"}' % state
    response = requests.request('POST', f'{BASE_URL}api/client/servers/{server}/power', data=payload,
                                headers=headers_client)
    print(response.text)
