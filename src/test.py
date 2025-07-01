from utils.config import *
from pprint import pprint
from dotenv import load_dotenv
import os
from utils.oa import demo
# pprint(get_config())
load_dotenv()
sf_models, sf_configs = get_models('SF')
print(sf_models)
# pprint(get_full_models())
pprint(get_model_info('DeepSeek-r1'))

# demo('GPT-4dot1-mini')