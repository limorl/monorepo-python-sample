import json
from typing import Any


def lambda_handler(event, context) -> Any:  # noqa: ANN001, ARG001
    return {
        'statusCode': 200,
        'body': json.dumps('Hello World!')
    }
