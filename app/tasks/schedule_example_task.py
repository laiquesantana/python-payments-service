# This module contains a script to schedule and run example tasks using asyncio.

# Functions:
# - run_task(job_args: Namespace): Asynchronously runs the scheduled task.
# - parse_args(raw_args: list) -> Namespace: Parses command line arguments.

# Usage:
# - This script can be executed directly from the command line. It parses the provided arguments and runs the specified task.

# Example:
#     $ python schedule_example_task.py --type long_time

# Modules:
# - asyncio: Provides support for asynchronous programming.
# - sys: Provides access to some variables used or maintained by the interpreter.
# - argparse: Provides a command-line argument parsing functionality.
# - app.config.structlog: Custom logging configuration for the application.
import asyncio
import sys
from argparse import ArgumentParser, Namespace

from app.config.structlog import get_struct_logger

logger = get_struct_logger(__name__)


async def run_task(job_args: Namespace):
    """Runner of schedule task.

    Args:
    -   job_args(`ArgumentParser`) : Argument received from command line

    """
    # TODO: add event to trigger example task
    _type = job_args.type.value
    logger.info(f"Running job - {_type} - Starting")
    logger.info(f"Running job - {_type} - Finishing")


def parse_args(raw_args: list) -> Namespace:
    """Parse arguments from command line.

    Args:
    -   raw_args(`list`) - List of arguments from command line

    Returns:
    -   `Namespace` - Parsed arguments

    """
    parser = ArgumentParser(
        description="""This script scheduler the balance mass for organizations."""
    )
    parser.add_argument(
        "-t",
        "--type",
        dest="type",
        type=str,
        default="type",
        help="Type of example task. Default value is long_time -> every 6 hours",
    )
    return parser.parse_args(raw_args)


if __name__ == "__main__":  # pragma: no cover
    args = parse_args(sys.argv[1:])
    asyncio.run(run_task(args))
