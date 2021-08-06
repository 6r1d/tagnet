"""
This module contains code for
configuring commandline argument support and
related :code:`argparse` actions.
"""

from argparse import ArgumentParser, FileType, Action as ArgparseAction
from .filtering import parse_number_filter
# Needed by ReadableDirectoryAction
from os.path import isdir
from os import access, R_OK

class NumberFilterAction(ArgparseAction):
    """
    An :code:`argparse.Action` subclass that validates the number filters.
    Accepts inputs like :code:`<x`, :code:`= x` or :code:`>=x`, where :code:`x` is an integer.

    Ignores a space in the middle.

    Raises:

        ValueError: if an incorrect format is provided
    """
    def __call__(self, parser, namespace, values, option_string=None):
        number_filter = parse_number_filter(values)
        if number_filter is not None:
            setattr(
                namespace,
                self.dest,
                number_filter
            )
        else:
            exception_str = """Wrong number filter value: {}.
            Provide an input like \"<x\", \"= x\" or \">=x\", where x is an integer."""
            raise ValueError(exception_str.format(values))

class ReadableDirectoryAction(ArgparseAction):
    """
    An :code:`argparse.Action` subclass that
    checks if a directory is readable.

    Raises:

        ArgumentTypeError: if a path is invalid
        ArgumentTypeError: if a directory is unreadable
    """
    def __call__(self, parser, namespace, values, option_string=None):
        if not isdir(values):
            raise argparse.ArgumentTypeError("{0} is an invalid path".format(values))
        if access(values, R_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError("{0} can not be accessed".format(values))

def configure_parser():
    """
    Configures :code:`argparse` to accept arguments needed by
    the :code:`tagnet` utility like "path", "output_file",
    "mode", "filter", etc.
    """
    parser = ArgumentParser(description='Tagnet utility.')
    parser.add_argument(
        '--path',
        help='A prompt directory path containing one or more of newline-delimited files',
        action=ReadableDirectoryAction
    )
    parser.add_argument(
        '--output_file',
        help='An output file for a JSON graph',
        type=FileType('w', encoding='utf-8')
    )
    parser.add_argument(
        '--mode',
        help='Utility mode.',
        choices=['count_tags', 'display_graph', 'export_graph']
    )
    parser.add_argument(
        '--filter',
        help='Filter for tag counting.',
        action=NumberFilterAction
    )
    return parser
