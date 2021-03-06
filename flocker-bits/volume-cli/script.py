import argparse
import os
from client import get_client
from volume_cli import move_or_create, detach, delete
from twisted.internet.task import react

MINIMUM_DATASET_SIZE = 67108864
GIGABYTE = 1024*1024*1024
SIZE_UNITS = {
    "gb": GIGABYTE,
    "gigabyte": GIGABYTE
}


def get_constants():
    values = {
        'target_port': 4523
    }
    return values


def get_environment():
    env_map = {
        'target_hostname': 'FLOCKER_CONTROL_SERVICE_ENDPOINT'
    }
    values = {}

    for property_name, env_name in env_map.iteritems():
        env_value = os.getenv(env_name)
        if env_value is None:
            raise Exception("%s env variable is required" % (env_name))
        values[property_name] = env_value

    return values


def get_arguments():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name')

    parser_create = subparsers.add_parser(
        'move_or_create',
        description=(
            "Move or create a Flocker dataset "
            "and wait until it shows up in /v1/state/datasets"
        )
    )

    parser_create.add_argument(
        '--dataset-uuid',
        dest='dataset_uuid',
        type=str,
        required=False,
        help='the UUID of the dataset'
    )
    parser_create.add_argument(
        '--dataset-name',
        dest='dataset_name',
        type=str,
        required=False,
        help='the name of the dataset'
    )
    parser_create.add_argument(
        '--host-uuid',
        dest='host_uuid',
        type=str,
        required=True,
        help='the UUID of the host for the dataset'
    )
    parser_create.add_argument(
        '--size',
        dest='size',
        type=int,
        required=False,
        help='the size of the dataset in bytes'
    )
    parser_create.add_argument(
        '--size-units',
        dest='size_units',
        type=str,
        required=False,
        help='the units of the size (bytes, gb)'
    )

    parser_delete = subparsers.add_parser(
        'delete',
        description=(
            "Delete a Flocker dataset "
            "and wait until it dissappears from /v1/state/datasets"
        )
    )

    parser_delete.add_argument(
        '--dataset-uuid',
        dest='dataset_uuid',
        type=str,
        required=False,
        help='the UUID of the dataset'
    )
    parser_delete.add_argument(
        '--dataset-name',
        dest='dataset_name',
        type=str,
        required=False,
        help='the name of the dataset'
    )


    parser_detach = subparsers.add_parser(
        'detach',
        description=(
            "Detach a Flocker dataset "
            "and wait until it detaches."
        )
    )

    parser_detach.add_argument(
        '--dataset-uuid',
        dest='dataset_uuid',
        type=str,
        required=False,
        help='the UUID of the dataset'
    )
    parser_detach.add_argument(
        '--dataset-name',
        dest='dataset_name',
        type=str,
        required=False,
        help='the name of the dataset'
    )

    args = parser.parse_args()
    return vars(args)


def get_settings():
    """
    Combine the environment settings with the command line arguments into one
    dict.
    """
    constants = get_constants()
    env = get_environment()
    args = get_arguments()
    if "size_units" in args and args["size_units"] is not None:
        size_units_value = args["size_units"].lower()
        if size_units_value in SIZE_UNITS:
            if "size" in args and args["size"] is not None:
                units = SIZE_UNITS[size_units_value]
                args["size"] = args["size"] * units
    if "dataset_uuid" not in args or args["dataset_uuid"] is None:
        if "dataset_name" not in args or args["dataset_name"] is None:
            raise Exception("either dataset-uuid or dataset-name is required")
    # dataset_name takes priority over dataset_uuid
    if "dataset_name" in args and args["dataset_name"] is not None:
        args["dataset_uuid"] = None
    settings = dict(env.items() + args.items() + constants.items())
    return settings


SUBCOMMANDS = {
    'move_or_create': move_or_create,
    'detach': detach,
    'delete': delete,
}


def main(reactor):
    settings = get_settings()
    client = get_client()
    return SUBCOMMANDS[settings['subparser_name']](settings, client)

if __name__ == "__main__":
    react(main)
