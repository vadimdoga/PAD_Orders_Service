import os


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
