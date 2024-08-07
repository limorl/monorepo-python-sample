import logging
from typing import Any

import boto3
from botocore.exceptions import ClientError

from configuration.secret import parse_secret_value, try_get_secret_name

logger = logging.getLogger()


def create_secret_manager_client(region: str, endpoint_url: str | None = None) -> any:
    options: dict = {'region_name': region}
    if endpoint_url:
        options['endpoint_url'] = endpoint_url

    return boto3.client('secretsmanager', **options)


def secrets_manager_get_secret_value(secretesmanager: Any, secret_config_val: str) -> str:
    secret_name = try_get_secret_name(secret_config_val)

    try:
        response = secretesmanager.get_secret_value(SecretId=secret_name)
        # secrets created by secrets manager console
        secret_string = response.get('SecretString')
        secret_value = secret_string and parse_secret_value(secret_string)

        if not secret_value:
            # secret was created in cli
            secret_binary = response.get('SecretBinary')
            secret_value = secret_binary and parse_secret_value(secret_binary.decode('utf-8'))
        if not secret_value:
            raise ValueError(
                f'Secrets Manager failed to retrieve secret {secret_name}. Both SecretString and SecretBinary are None.'
            )

    except ClientError:
        logger.exception(f'Secrets Manager failed to retrieve secret {secret_name}.')
        raise

    return secret_value
