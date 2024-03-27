import argparse
import sys
from jira_notifications.helper import Helper
from jira_notifications.logger import get_logger
from jira_notifications.triggers import Triggers
import sched
import time

def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Jira Notification ", allow_abbrev=False)
    parser.add_argument("-c", "--config", dest="config_file", help="Config YAML file")
    parser.add_argument("-g", "--generate-config", dest="generate_config",
                        help="Generate a sample config.yaml file")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const="INFO",
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const="DEBUG",
    )
    return parser.parse_args(args)


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """

    args = parse_args(args)
    if args.loglevel:
        logger = get_logger(__name__, args.loglevel)
    else:
        logger = get_logger(__name__)

    helper = Helper(logger)
    if args.generate_config:
        helper.generate_sample_config(args.generate_config)
        logger.info("Sample config.yaml generated. Please customize it with your settings.")
        sys.exit(0)

    logger.info("Loading config...")
    config = helper.load_config(args.config_file)
    trigger = Triggers(config, logger)

    scheduler = sched.scheduler(time.time, time.sleep)
    repeated = False
    while True:
        scheduler.enter(5, 1, trigger.jira_daily_toast, (repeated,))
        scheduler.enter(config.get("toast_time_seconds"), 1, trigger.jira_routine_toast, ())
        scheduler.run()
        if not helper.is_time_equal_to_input(config.get("daily_toast_time")) and repeated:
            repeated = False
        else:
            repeated = True

def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])

if __name__ == "__main__":
    run()
