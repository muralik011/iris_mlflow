import json


class JSONParser:
    def __init__(self, file):
        self.file = file

    def read_json(self):
        try:
            with open(self.file, 'r') as json_file:
                json_data = json.load(json_file)
        except FileNotFoundError as fnf_err:
            print(fnf_err)
            json_data = None
        except json.decoder.JSONDecodeError as json_err:
            print(json_err)
            json_data = None
        else:
            print(f'json file {self.file} read successful')
        return json_data

    def get_values(self, keys: list):
        json_data = self.read_json()
        value = None
        if json_data is not None:
            try:
                value = json_data[keys[0]]
                for key in keys[1:]:
                    value = value[key]
            except KeyError as key_err:
                print(f'key error: {key_err}')
                value = None
            except TypeError as type_err:
                print(f'type error: {type_err}')
                value = None
            else:
                print(f'json value {keys} read successful')
        return value
