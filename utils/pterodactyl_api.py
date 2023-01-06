import disnake as discord
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
}

servers = {}
black_listed_servers = ["27ce74ca", "07571d6c", "6f970cf0", "f43119da", "2c5f4b02"]
server_states = {"running": "✅", "offline": "❌", "starting": "⏳", "stopping": "⏳"}


async def get_server_status(server):
    response = requests.request('GET', f'{BASE_URL}api/client/servers/{server}/resources', headers=headers_client)
    data = response.json()
    state = data['attributes']['current_state']
    return server_states[state]


async def servers_embed():
    the_embed = discord.Embed(title="Server Status", colour=discord.Color.blurple())
    for name, server_id in servers.items():
        the_embed.add_field(inline=True, name=name, value=f"Status: {await get_server_status(server_id)}")
    if len(servers) % 3 == 1:
        print(len(servers))
        the_embed.add_field(inline=True, name="᲼", value="᲼")
    return the_embed


def get_servers():
    response = requests.request('GET', f'{BASE_URL}api/application/servers', headers=headers_application)
    data = response.json()
    servers.clear()
    for f in data['data']:
        server_name = f['attributes']['name']
        server_uuid = f['attributes']['identifier']
        if not black_listed_servers.__contains__(server_uuid):
            servers.update({server_name: server_uuid})


async def change_power_state(server, state):
    payload = f'{{"signal": "{state}"}}'
    requests.request('POST', f'{BASE_URL}api/client/servers/{server}/power', data=payload,
                     headers=headers_client)
