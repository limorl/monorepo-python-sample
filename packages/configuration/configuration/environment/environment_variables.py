from enum import Enum
from dotenv import load_dotenv
import os


class Platform(Enum):
    AWS = 'AWS'
    LOCAL = 'local'


class Environment(Enum):
    PROD = 'prod'           # production
    STAGING = 'staging'     # remote staging env
    DEV = 'dev'             # local dev/ci environment

def is_cloud_platform(platform: Platform):
    return platform == Platform.AWS

class EnvironmentVariables:

    def __init__(self, dotenvpath: str = None):
        if dotenvpath:
            load_dotenv(dotenvpath) # loads environment variables from .env file under project's folder

        self.platform = Platform(os.getenv('PLATFORM')) if os.getenv('PLATFORM') else None
        self.region: str = os.getenv('REGION')
        self.cloud_endpoint_override: str = os.getenv('CLOUD_ENDPOINT_OVERRIDE')
        self.service_name: str = os.getenv('SERVICE_NAME')
        self.environment = Environment(os.getenv('ENVIRONMENT')) if os.getenv('ENVIRONMENT') else None
        self.local_configuration_folder = os.getenv('LOCAL_CONFIGURATION_FOLDER')

        if is_cloud_platform(self.platform) and not self.service_name:
            raise ValueError('Missing service name for cloud platform')


def reset_environment_variables():
    if os.getenv('PLATFORM'): 
        del os.environ['PLATFORM']
    if os.getenv('REGION'): 
        del os.environ['REGION']
    if os.getenv('CLOUD_ENDPOINT_OVERRIDE'): 
        del os.environ['CLOUD_ENDPOINT_OVERRIDE']
    if os.getenv('SERVICE_NAME'): 
        del os.environ['SERVICE_NAME']
    if os.getenv('ENVIRONMENT'): 
        del os.environ['ENVIRONMENT']
    if os.getenv('LOCAL_CONFIGURATION_FOLDER'): 
        del os.environ['LOCAL_CONFIGURATION_FOLDER']
