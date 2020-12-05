import logging.config
import os
import uuid

import yaml

with open('log_config.yaml', 'r') as log_config_file:
    if not os.path.exists('logs'):
        os.makedirs('logs')
    log_config = yaml.safe_load(log_config_file.read())
    logging.config.dictConfig(log_config)


def check_file_existance(file_path):
    """Check if 'db_config.ini' file exists"""

    if (not os.path.exists(file_path)):
        print(f"{file_path} does not exist!")
        os._exit(0)


def get_configs(config, section):
    """Get credentials from 'db_config.ini' file"""

    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


def generate_uuid_key():
    return str(uuid.uuid4())


def validate_list_keys(keys_list, key_type, key_name):
    """Validate list type"""
    for key in keys_list:
        if not isinstance(key, key_type):
            raise TypeError(
                f"Field {key_name} must contain objects of type {str(key_type)} Check documentation more carefully!")


def validate_keys(json_data, dict_keys):
    """Validate JSON name, type and existance"""

    json_keys = json_data.keys()
    list_requisite_keys = dict_keys.keys()

    missing_keys = []
    extra_keys = []

    check_instance = True

    for key_name in dict_keys:
        key_name = key_name
        key_type = dict_keys[key_name]["type"]
        key_null = dict_keys[key_name]["null"]

        # check for missing keys in JSON
        if key_name not in json_keys:
            missing_keys.append(key_name)
            check_instance = False
            continue

        # check instance of the key
        json_value = json_data[key_name]

        if not isinstance(json_value, key_type) and check_instance:
            if key_null:
                if json_value != None:
                    raise TypeError(
                        f"Field {key_name} must be of type {str(key_type)}")
            else:
                raise TypeError(
                    f"Field {key_name} must be of type {str(key_type)}")

    for key_name in json_data:
        # check for extra keys in JSON
        key_name = key_name
        if key_name not in list_requisite_keys:
            extra_keys.append(key_name)

    if extra_keys != []:
        raise KeyError("Remove the following keys: " +
                       ",".join(extra_keys))

    if missing_keys != []:
        raise KeyError(",".join(
            missing_keys) + " keys missing from json")
