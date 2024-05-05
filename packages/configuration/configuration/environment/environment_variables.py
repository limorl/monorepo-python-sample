from enum import Enum
from dotenv import load_dotenv
import os


class Platform(Enum):
    AWS = 'AWS'
    LOCAL = 'local'


class Stage(Enum):
    PROD = 'prod'           # production
    STAGING = 'staging'     # remote staging env
    DEV = 'dev'             # local dev/ci environment


def is_cloud_platform(platform: Platform):
    return platform == Platform.AWS


class EnvironmentVariables:
    #_default_platform: Platform = Platform.AWS
    #_default_region: str = 'us-east-1'
    #_default_stage: str = 'prod'

    def __init__(self, dotenvpath: str = None):
        if dotenvpath:
            load_dotenv(dotenvpath)  # loads environment variables from .env file under project's folder

        self.platform = Platform(os.getenv('PLATFORM')) if os.getenv('PLATFORM') else None
        self.region: str = os.getenv('REGION')
        
        if not self.region and self.platform == Platform.AWS:
            self.region: str = os.getenv('AWS_REGION')
       
        self.cloud_endpoint_override: str = os.getenv('CLOUD_ENDPOINT_OVERRIDE')
        self.service_name: str = os.getenv('SERVICE_NAME')
        self.stage = Stage(os.getenv('STAGE')) if os.getenv('STAGE') else None
        self.local_configuration_folder = os.getenv('LOCAL_CONFIGURATION_FOLDER')

        if is_cloud_platform(self.platform) and not self.service_name:
            raise ValueError('Missing service name for cloud platform')
        
    def __str__(self):
        return str(self.__class__.__name__) + ": " + str(self.__dict__)


def reset_environment_variables():
    if os.getenv('PLATFORM'):
        del os.environ['PLATFORM']
    if os.getenv('REGION'):
        del os.environ['REGION']
    if os.getenv('CLOUD_ENDPOINT_OVERRIDE'):
        del os.environ['CLOUD_ENDPOINT_OVERRIDE']
    if os.getenv('SERVICE_NAME'):
        del os.environ['SERVICE_NAME']
    if os.getenv('STAGE'):
        del os.environ['STAGE']
    if os.getenv('LOCAL_CONFIGURATION_FOLDER'):
        del os.environ['LOCAL_CONFIGURATION_FOLDER']
