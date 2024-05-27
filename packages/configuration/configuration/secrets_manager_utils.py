import logging
from botocore.exceptions import ClientError
from typing import Any
from configuration.secret import is_secret, parse_secret_value

SECRET_PREFIX = 'secret:'

logger = logging.getLogger()


def secrets_manager_get_secret_value(secretesmanager: Any, secret_config_val: str) -> str:
    secret_name = secret_config_val and secret_config_val.replace(SECRET_PREFIX, '')

    try:
        response = secretesmanager.get_secret_value(SecretId=secret_name)
        secret_value = parse_secret_value(response.get('SecretString'))  # if secret were created by secrets manager console

        if not secret_value:
            # secret was created in cli
            secret_value = response.get('SecretBinary') and parse_secret_value(response.get('SecretBinary').decode('utf-8'))
        if not secret_value:
            raise ValueError((f"SSM failed to retrieve secret {secret_name}. Both SecretString and SecretBinary are None."))

    except ClientError as err:
        logger.error(f"SSM failed to retrieve secret {secret_name}. Error: {err}")
        raise err

    return secret_value
