# (c) Copyright contributors to the conversational-prompt-engineering project

# LICENSE: Apache License 2.0 (Apache-2.0)
# http://www.apache.org/licenses/LICENSE-2.0

import json
import os


def load_config(config_name):
    config_file_name = os.path.join("configs", f"{config_name}_config.json")
    try:
        with open(config_file_name, 'r') as fin:
            config = json.load(fin)
        # end with
    except:
        raise ValueError(f"Can't load {config}. Check if {config_file_name} exists.")
    return config
# end def