import os
import sys
from .app import app
from serverless_wsgi import handle_request

# Add the deployment package root directory to the Python path
package_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(package_root)


def handler(event, context):
    return handle_request(app, event, context)
