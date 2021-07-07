"""
Contains filtering-related functions.

Todo:

    elaborate
"""

from re import compile as re_compile

def parse_number_filter(in_str):
    """
    Parses number filters like "<x", "= x" or ">=x",
    where "x" is an integer.

    Returns:

        None if the format is wrong.

        A dict containing "condition" and
        "number" values.

    Example:

        >>> from lib.filtering import parse_number_filter
        >>> parse_number_filter('==10')
        {'condition': '=', 'number': '10'}
        >>> parse_number_filter('>= 5')
        {'condition': '>=', 'number': '5'}
        >>> parse_number_filter('<= 12')
        {'condition': '<=', 'number': '12'}
        >>> parse_number_filter('> 777')
        {'condition': '>', 'number': '777'}
    """
    re_prog = re_compile("(\<\=|\>\=|\<|\>|\=|\=\=)(\s*)(\d+)")
    prog_match = re_prog.match(in_str)
    result = None
    if prog_match is not None:
        result = {
            'condition': prog_match.groups()[0],
            'number': int(prog_match.groups()[2], 10)
        }
        # Replace '==' with '='
        if result['condition'] == '==':
            result['condition'] = '='
    return result
