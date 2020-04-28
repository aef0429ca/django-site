import os
import json

CONFIG_FILE = '/etc/config.json'

try:
    with open(CONFIG_FILE) as config_file:
        config = json.load(config_file)
        config['PROD']
        SECRET_KEY = config['SECRET_KEY']
    from .prod import *
    
     
except EnvironmentError:
    from .dev import *

