import json


class SecretsParser:
    def __init__(self):
        pass

    @staticmethod
    def read_secrets():
        try:
            with open('secrets.json', 'r') as secrets_json:
                secrets = json.load(secrets_json)
        except FileNotFoundError as fnf_err:
            print(fnf_err)
            secrets = None
        except json.decoder.JSONDecodeError as json_err:
            print(json_err)
            secrets = None
        return secrets

    def get_values(self, keys: list):
        secrets = self.read_secrets()
        value = None
        if secrets is not None:
            try:
                value = secrets[keys[0]]
                for key in keys[1:]:
                    value = value[key]
            except KeyError as key_err:
                print(key_err)
                value = None
            except TypeError as type_err:
                print(type_err)
                value = None
        return value
