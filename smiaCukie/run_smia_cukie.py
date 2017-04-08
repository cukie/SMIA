import argparse
import batch_runner
import logging
import parse_config
import sys


# makes logs more clear when we invoke from the command line
logger = logging.getLogger(__name__)


def batchRunnerFromConfigDict(config_dict):
    """Creates a BatchRunner instance from a given configuration dictionary mapping input parameters to values.
    See batch_runner.BatchRunner for an explanation of parameters.
    """

    base_dir = config_dict['base_dir']
    num_layers = config_dict['num_layers']
    num_masks = config_dict['num_masks']
    num_markers = config_dict['num_markers']
    mask_names = config_dict['mask_names']
    marker_names = config_dict['marker_names']
    output_path = config_dict['output_path']
    output_images = config_dict['output_images']
    output_thumbnails = config_dict['output_thumbnails']
    # We want this as a dictionary for faster lookups
    # TODO: this seems awkward.. right now it is maintained to keep
    # compatibility with BatchImage objects.
    white_list = {}
    for sentence in config_dict['overlay_white_list']:
        white_list[sentence] = sentence

    return batch_runner.BatchRunner(base_dir,
                                    num_layers,
                                    num_masks,
                                    num_markers,
                                    mask_names,
                                    marker_names,
                                    white_list,
                                    output_images,
                                    output_thumbnails,
                                    output_path)


def runSMIAFromConfig(config_file):
    """
    An entry point to the SMIA-CUKIE application.
    This will kick off a run as specified by the configuration file.

    :param string config_file: The absolute path to a config file.

    """

    # parse the json configuration file
    success, message, config_dict = parse_config.ParseConfig(config_file)
    if not success:
        logger.error(message)
        sys.exit(1)
    else:
        logger.info(message)

    # Get our BatchRunner Object
    batchRunner = batchRunnerFromConfigDict(config_dict)
    # Here's where the magic happens
    batchRunner.run()

    logger.info(
        "You have succesfully procesed: {0}".format(batchRunner.base_dir))
    logger.info("Results can be found in: {0}".format(batchRunner.output_path))


def run_smia_cukie(parsed_args):
    """
    Runs SMIA-CUKIE. An entry point from any caller(front end).

    :param argparse.Namespace parsed_args:

    """

    loggingLevel = logging.DEBUG if parsed_args.verbose else logging.INFO
    logging.basicConfig(level=loggingLevel)

    runSMIAFromConfig(parsed_args.config_file_name)

def get_args_namespace(arg_string=None):
    """A namespace based on arg_string or default sys.argv"""

    parser = argparse.ArgumentParser(
    description="Runs the SMIA-CUKIE software according to the given config file.")
    parser.add_argument("config_file_name",
                    help="The name of the text file containing the configuration for this run.",
                    type=str)
    parser.add_argument("--verbose",
                    help="Turn on verbose output. Equivalent to DEBUG level logging.",
                    action="store_true")

    if not arg_string:
        args = parser.parse_args()
    else:
        args = parser.parse_args(arg_string)

    return args

if __name__ == '__main__':
    """Run SMIA-CUKIE from the command line"""

    args = get_args_namespace()
    run_smia_cukie(args)
