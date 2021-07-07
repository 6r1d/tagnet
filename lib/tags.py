"""
This module contains:

* a generic tag processing class that corrects case,
  stores a tag list, counts tags
* a function that extracts a list of tags from a CLIP prompt string
"""

from collections import defaultdict
from .prompts import prompt_split

def extract_tags(prompt):
    """
    Extract a list of the tags from a single prompt.

    Parameters:

        prompt (str): a prompt for the CLIP neural network

    Example:

        >>> from lib.tags import extract_tags
        >>> extract_tags('.imagine the color clash ; HDR ; hyperrealistic ; contest winner')
        [
            'HDR',
            'hyperrealistic',
            'contest winner'
        ]
    """
    split_row = prompt_split(prompt, 1)
    # Fill tags if there are any
    if len(split_row) > 1:
        tags = prompt_split(split_row[1], 0)
    else:
        tags = []
    # Remove all empty string elements
    tags = list(filter(None, tags))
    return tags

class Tag_processor:
    """
    Used to store tag indices, proper tag cases, global count of the tags.

    Attributes:

        case_fix_dict (dict): associates the lowercase string with properly cased ones
        tag_list (list): a list of enumerated lowercase strings
        global_tag_count (int): a count of all the tags added
    """

    # Store initial case for each tag
    case_fix_dict = {}
    # Used to enumerate the tags
    tag_list = []
    # Counts tags
    tag_dict = defaultdict(int)
    # Full amount of all added tags
    global_tag_count = 0

    def get_tag_rank(self, tag_id):
        """
        Args:

            tag_id (int): a tag index

        Returns:

            a rank of a tag, the quotient of tag count divided by the global tag count
        """
        return self.tag_dict[ self.tag_list[tag_id] ] / self.global_tag_count

    def put_tag(self, tag):
        """
        Args:

            tag (str): a tag name, case-insensitive

        Returns:

            a tag ID

        Example:

            >>> from lib.tags import Tag_processor
            >>> tp = Tag_processor()
            >>> tp.put_tag('VFX')
            0
            >>> tp.put_tag('HDR')
            1
            >>> tp.put_tag('DSLR')
            2
        """
        # Store tag cases
        self.case_fix_dict[tag.lower()] = tag
        # Register a tag for indexing
        if tag.lower() not in self.tag_list: self.tag_list.append(tag.lower())
        # Update the counter for a given tag
        self.tag_dict[tag.lower()] += 1
        # Update a global tag count
        self.global_tag_count += 1
        return self.tag_list.index(tag.lower())

    def put_tags(self, tag_list):
        """
        Args:

            tag_list (list): a list of strings with tag names (case-insensitive)

        Returns:

            a list of tag IDs

        Example:

            >>> from lib.tags import Tag_processor
            >>> tp = Tag_processor()
            >>> tp.put_tags(['SFX', 'high detail', 'light transport sharpening'])
            [0, 1, 2]
        """
        # Prepare a list of tag numbers
        tag_numbers = []
        # Iterate tags, store tag cases, store tag numbers
        for tag in tag_list:
            tag_number = self.put_tag(tag)
            # Add numbers of tags to tag_numbers
            tag_numbers.append(tag_number)
        return tag_numbers

    def add_tags(self, tag_list):
        """
        Works like put_tags, but returns nothing

        Args:

            tag_list (list): a list of strings with tag names (case-insensitive)

        Example:

            >>> from lib.tags import Tag_processor
            >>> tp = Tag_processor()
            >>> tp.add_tags(['SFX', 'high detail', 'light transport sharpening'])
        """
        # Iterate tags, store tag cases, store tag numbers
        for tag in tag_list:
            tag_number = self.put_tag(tag)

    def get_tag_list(self):
        """
        Returns:

            A list of dictionaries with "id", "name" and "rank" attribute.
            ID is an integer,
            name is a string,
            a rank is a float value containing the quotient of tag count divided by the global tag count.

        Example:

            >>> from lib.tags import Tag_processor
            >>> tp = Tag_processor()
            >>> tp.put_tags(['landscape', 'beautiful', 'neon'])
            [0, 1, 2]
            >>> tp.get_tag_list()
            [
                {'id': 0, 'name': 'landscape', 'rank': 0.3333333333333333},
                {'id': 1, 'name': 'beautiful', 'rank': 0.3333333333333333},
                {'id': 2, 'name': 'neon', 'rank': 0.3333333333333333}
            ]
        """
        return [
            {
                # Unique ID of a tag
                'id': tag_id,
                # Name of a tag
                'name': self.case_fix_dict[ self.tag_list[tag_id] ],
                # Popularity of a tag (occurence count divided by the global_tag_count)
                # 'rank': self.tag_dict[ self.tag_list[tag_id] ] / self.global_tag_count # TODO remove
                'rank': self.get_tag_rank(tag_id)
            }
            for tag_id
            in range(len(self.tag_list))
        ]

    def get_tag_numbers(self):
        """
        Iterate a list of tags with their count.

        Returns:

            a list of tuples, containing tag names and numbers

        Example:

            >>> from lib.tags import Tag_processor
            >>> tp = Tag_processor()
            >>> tp.put_tags(['landscape', 'beautiful', 'neon'])
            [0, 1, 2]
            >>> tp.get_tag_numbers()
            [('landscape', 1), ('beautiful', 1), ('neon', 1)]
        """
        return sorted(
            [(self.case_fix_dict[item[0]], item[1]) for item in self.tag_dict.items()],
            key=lambda k_v: k_v[1],
            reverse=True
        )
