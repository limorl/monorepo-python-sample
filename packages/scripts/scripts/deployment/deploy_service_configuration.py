
import argparse
import logging
from configuration.app_config_utils import app_config_deploy_service_configuration
from environment.service_environment import Platform, Stage


logger = logging.getLogger()


def deploy_service_configuration(service_name: str, platform: Platform, stage: Stage, region: str) -> None:
    app_config_deploy_service_configuration(service_name, Platform(platform), Stage(stage), region)


def _create_arg_parser():
    parser = argparse.ArgumentParser(prog='deploy_service_configuration.py', description='Deploy service configuration to AWS AppConfig')
    parser.add_argument('--service-name', type=str, required=True, help='The name of the service package, for example: greeting')
    parser.add_argument('--platform', type=str, required=False, default='AWS', help='The platform to deploy to, currently only AWS is supported')
    parser.add_argument('--stage', type=str, required=True, help='Stage in [prod|dev|staging]')
    parser.add_argument('--region', type=str, required=True, help='Region e.g., us-east-1')
    return parser


def main():
    parser = _create_arg_parser()
    args = parser.parse_args()

    deploy_service_configuration(args.service_name, Platform(args.platform), Stage(args.stage), args.region)


if __name__ == "__main__":
    main()
