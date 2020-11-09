from ruamel.yaml import YAML
import os
import sys

# This class contains all methods to handle YAML files
class YAMLUtils(object):
    # File Name
    FILE_NAME = 'financial-institution-config.yaml'

    # Method reads YAML File
    @staticmethod
    def readYAML(file_name):
        yaml = YAML()
        if (os.path.isfile(file_name)):
            with open(file_name, "r") as stream:
                try:
                    data = yaml.load(stream)['root']
                    return data
                except yaml.YAMLError as exc:
                    print("YAML Error: " + exc)
        else:
            print("File <" + file_name + "> does not exist!")
            return None

    # Method to make updates to the total count of a given bank's accounts
    @staticmethod
    def writeYAML(file_name, bank_name, update):
        yaml = YAML()
        yaml.preserve_quotes = True
        with open(file_name, "r") as stream:
            data = yaml.load(stream)
        for bank in data['root']:
            if bank['name'] == bank_name:
                bank['total_count'] = update
                break
        with open(file_name, 'w') as f:
            yaml.dump(data, f)