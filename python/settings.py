import os
from pathlib import Path
path = os.path.join(Path(__file__).parents[1], 'tokens')

def token():
    with open(f"{path}\\vk_token_communities.txt", 'r') as token_vk_communities:
        token_vk_communities = token_vk_communities.read().strip()
    with open(f"{path}\\vk_token.txt", 'r') as vk_token:
        vk_token = vk_token.read().strip()
    return [token_vk_communities, vk_token]

