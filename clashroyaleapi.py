import requests
import os

class clashRoyale:

    def __init__(self):

        self.headers = headers = {
            'Accept': 'application/json',
            'authorization': f'Bearer {os.environ["clash-royale-token"]}'
        }

    def get_clan(self):
        response = requests.get(
            'https://api.clashroyale.com/v1/clans/%23Y0PCJJGG', headers=self.headers)
        user_json = response.json()
        return user_json

    def clan_members(self):
        response = requests.get(
            'https://api.clashroyale.com/v1/clans/%23Y0PCJJGG', headers=self.headers)
        user_json = response.json()
        return user_json["memberList"]


