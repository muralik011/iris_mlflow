import json
import os


class SecretsParser:
    def __init__(self):
        pass

    @staticmethod
    def read_secrets():
        with open('secrets.json', 'r') as secrets_json:
            secrets = json.load(secrets_json)
        return secrets

    def get_values(self, keys: list):
        secrets = self.read_secrets()
        value = secrets[keys[0]]
        for key in keys[1:]:
            value = value[key]
        return value
