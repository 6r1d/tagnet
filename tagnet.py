#!/usr/bin/env python3

"""
Tag network, an entry point file for the "CLIP tags exploration" project.

Allows you to use these modes:

* :code:`count_tags` - simply displays tags found in a certain path, allows filtering
* :code:`display_graph` - displays a graph using Matplotlib's WxWidgets interface
* :code:`export_graph` - exports graph contents as a JSON file
"""

from lib.cmd_args import configure_parser
from lib.process import process_dir

def main():
    """
    * Loads a pre-configured parser
    * Calls an entry-point function if a mode is known
    * Displays an error and provided arguments otherwise 
    """
    parser = configure_parser()
    args = parser.parse_args()

    if "mode" in args and args.mode in ['count_tags', 'display_graph', 'export_graph']:
        process_dir(args)
    else:
        # Display all available arguments for an unknown mode.
        print('Error: unknown mode! Command-line arguments:')
        for arg in vars(args):
            print(arg, getattr(args, arg))
        print('Exiting')

if __name__ == '__main__':
    main()
