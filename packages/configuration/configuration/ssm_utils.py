from botocore.exceptions import ClientError
import logging

SECRET_PREFIX = 'ssm:'

logger = logging.getLogger()


def is_secret(val: str) -> bool:
    return isinstance(val, str) and val.startswith(SECRET_PREFIX)


def ssm_get_secret_value(ssm, secret_config_val: str) -> str:
    secret_name = secret_config_val and secret_config_val.replace(SECRET_PREFIX, '')

    try:
        response = ssm.get_secret_value(SecretId=secret_name)
        secret_value = response.get('SecretString')  # if secret were created by ssm console

        if not secret_value:
            # secret was created in cli
            secret_value = response.get('SecretBinary') and response.get('SecretBinary').decode('utf-8')
        if not secret_value:
            raise ValueError((f"SSM failed to retrieve secret {secret_name}. Both SecretString and SecretBinary are None."))

    except ClientError as err:
        logger.error(f"SSM failed to retrieve secret {secret_name}. Error: {err}")
        raise err

    return secret_value
