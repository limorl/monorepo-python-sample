from enum import Enum
from dotenv import load_dotenv
import os


AWS_PRIMARY_REGION_PROD = 'us-east-1'
AWS_PRIMARY_REGION_DEV = 'us-east-1'

class Platform(Enum):
    AWS = 'AWS'
    LOCAL = 'local'


class Stage(Enum):
    PROD = 'prod'           # production
    STAGING = 'staging'     # remote staging env
    DEV = 'dev'             # local dev/ci environment


def is_cloud_platform(platform: Platform):
    return platform == Platform.AWS


class ServiceEnvironment:

    def __init__(self, dotenvpath: str = None):
        if dotenvpath:
            load_dotenv(dotenvpath)  # loads environment variables from .env file under project's folder

        self.platform: Platform = os.getenv('PLATFORM') and Platform(os.getenv('PLATFORM'))
        self.stage: Stage = os.getenv('STAGE') and Stage(os.getenv('STAGE'))

        self.region: str = os.getenv('REGION')
        if not self.region and self.platform == Platform.AWS:
            self.region: str = os.getenv('AWS_REGION')

        # Primary region is where account shared resources are provisioned, such as AppConfig, SecretsManager, ECR
        # You can set it according to the stage, e.g., return 'us-east-1' if stage == Stage.PROD else 'us-west-2'
        self.primary_region: str = get_primary_region(self.stage)

        self.cloud_endpoint_override: str = os.getenv('CLOUD_ENDPOINT_OVERRIDE')
        self.service_name: str = os.getenv('SERVICE_NAME')

        default_configuration_folder = os.path.join(os.getcwd(), 'config')
        self.local_configuration_folder = os.getenv('LOCAL_CONFIGURATION_FOLDER') or default_configuration_folder

        if is_cloud_platform(self.platform) and not self.service_name:
            raise ValueError('Missing service name for cloud platform')

    def __str__(self):
        return str(self.__class__.__name__) + ": " + str(self.__dict__)

def get_primary_region(stage: Stage) -> str:
    if stage:
        return AWS_PRIMARY_REGION_PROD if stage == Stage.PROD else AWS_PRIMARY_REGION_DEV
    return None

def clear_service_environment():
    if os.getenv('PLATFORM'):
        del os.environ['PLATFORM']
    if os.getenv('REGION'):
        del os.environ['REGION']
    if os.getenv('STAGE'):
        del os.environ['STAGE']
    if os.getenv('CLOUD_ENDPOINT_OVERRIDE'):
        del os.environ['CLOUD_ENDPOINT_OVERRIDE']
    if os.getenv('SERVICE_NAME'):
        del os.environ['SERVICE_NAME']
    if os.getenv('LOCAL_CONFIGURATION_FOLDER'):
        del os.environ['LOCAL_CONFIGURATION_FOLDER']

def restore_local_dev_service_environment():
    clear_service_environment()
    os.environ['PLAFORM'] = Platform.LOCAL.value
    os.environ['STAGE'] = Stage.DEV.value
    os.environ['CLOUD_ENDPOINT_OVERRIDE'] = 'http://localhost:4566'
