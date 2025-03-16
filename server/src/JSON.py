import json
import logging

class JSON:
    @staticmethod
    def get_json(filename):
        try:
            with open(filename, 'r+', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            raise Exception(f"Error reading JSON file {filename}") from e

    @staticmethod
    def generate_json(file_new, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(file_new)
        except Exception as e:
            raise Exception(f"Error generating JSON file {filename}") from e

    @staticmethod
    def set_json(file_new, filename, indent=4):
        try:
            file = open(filename, 'w+', encoding='utf-8') # il + per evitare di usare file.truncate() dopo
            json.dump(file_new, file, indent=indent)
            file.close()
            # logging.info(f"JSON modified: {filename}")
            print(f"JSON modified: {filename}")
        except Exception as e:
            raise Exception(f"Error modifying JSON file {filename}") from e