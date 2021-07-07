"""
Contains a function to load prompts from available files.
"""

from os import listdir
from os.path import isfile, join, abspath
from re import split

def load_prompts(dir_path):
    """
    Looks up a directory path, takes a full path for it,
    lists for directory contents and loads all available prompts.

    Example:

        >>> from lib.prompts import load_prompts
        >>> prompts = load_prompts('./prompts')
        >>> prompts[-3:]
        [
            '.imagine α-pinene pool ; vray ; PBR ; HDR ; closeup ; DSLR ; hyperrealistic',
            '.imagine omicron ; vray ; hdr illumination ; contest winner',
            '.imagine the night ; vray ; isonoise ; contest winner ; highly sought art'
        ]

    Args:

        dir_path (str): a path to the prompt directory

    Returns:

        a list of strings containing CLIP prompts
    """
    rows = ""
    # Build a file list
    file_list = [join(dir_path, f) for f in listdir(dir_path) if isfile(join(dir_path, f))]
    # Load prompts from a file
    for file_path in file_list:
        # Load a file
        with open(file_path, 'r') as prompts_file:
            rows += prompts_file.read().strip()
            rows += "\n"
    # Remove the last endline
    rows = rows.strip()
    # Remove duplicates and sort
    result = sorted(
        list(set(rows.splitlines()))
    )
    return result

def prompt_split(prompt, maxsplit=0):
    """
    Split to unique prompts.

    Examples:

        >>> prompt_split('.imagine the Fresnel lens ; in fine detail ; rendered in charcoal | realistic', 1)
        ['.imagine the Fresnel lens', 'in fine detail ; rendered in charcoal | realistic']

        >>> prompt_split('in fine detail ; rendered in charcoal | realistic')
        ['in fine detail', 'rendered in charcoal', 'realistic']

    Args:

        prompt (str): a prompt to split
        maxsplit (int): a maximum number of splits

    Returns:

        a list of strings containing prompt elements
    """
    div = split('[;|,]', prompt, maxsplit=maxsplit)
    return list(map(str.strip, div))
