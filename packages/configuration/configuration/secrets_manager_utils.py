import json
import logging
from botocore.exceptions import ClientError
from typing import Dict, Any

SECRET_PREFIX = 'secret:'

logger = logging.getLogger()


def is_secret(val: str) -> bool:
    return isinstance(val, str) and val.startswith(SECRET_PREFIX)


def secrets_manager_get_secret_value(secretesmanager: Any, secret_config_val: str) -> str:
    secret_name = secret_config_val and secret_config_val.replace(SECRET_PREFIX, '')

    try:
        response = secretesmanager.get_secret_value(SecretId=secret_name)
        secret_value = _parse_secret(response.get('SecretString'))  # if secret were created by secrets manager console

        if not secret_value:
            # secret was created in cli
            secret_value = response.get('SecretBinary') and _parse_secret(response.get('SecretBinary').decode('utf-8'))
        if not secret_value:
            raise ValueError((f"SSM failed to retrieve secret {secret_name}. Both SecretString and SecretBinary are None."))

    except ClientError as err:
        logger.error(f"SSM failed to retrieve secret {secret_name}. Error: {err}")
        raise err

    return secret_value


def _parse_secret(text: str) -> str | Dict[str, Any]:
    try:
        if text and text.startswith('{') and text.endswith('}'):
            return json.loads(text)
        else:
            return text
    except ValueError:
        return None