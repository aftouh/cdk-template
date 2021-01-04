from typing import Dict

from benedict import benedict


# Load configuration and merge common conf and specific stage config.
def load_config(stage: str) -> Dict:
    # Load common file
    try:
        common_config = benedict.from_yaml('config/common.yaml')
    except ValueError:
        print('No config found in config/common.yaml.')
        common_config = benedict([])

    # Load stage specific file
    try:
        env_config = benedict.from_yaml('config/' + stage + '.yaml')
    except ValueError:
        print('No config found in config/' + stage + '.yaml')
        env_config = benedict([])

    # merge the configs
    common_config.merge(env_config)

    # extract stage to set env
    common_config['stage'] = stage

    return common_config
