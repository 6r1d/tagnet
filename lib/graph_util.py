"""
Graph-related utility functions for CLIP neural network tags.
"""

from itertools import permutations
from collections import defaultdict
from networkx import Graph

def build_graph(tp, pmgr):
    """
    Builds a NetworkX graph with vertices from Tag_graph_processor
    and edges from Pair_mgr.

    Args:

        tp (Tag_processor): instance of a Tag_graph_processor
        pmgr (Pair_mgr): instance of Pair_mgr

    Returns:

        NetworkX Graph instance 
    """
    # Prepare a graph
    G = Graph()
    # Fill graph nodes
    for current_tag in tp.get_tag_list():
        G.add_node(current_tag['id'], name=current_tag['name'], rank=current_tag['rank'])
    # Fill graph edges
    for item in pmgr.get_list():
        G.add_edges_from([
            (item['edge'][0], item['edge'][1], {'weight': item['weight']})
        ])
    # Return the graph
    return G

def generate_pairs(tag_numbers):
    """
    Converts a list of tag numbers to list of number pairs
    to create bidirectional graph edges.

    Returns:

        a list of tuples; tuples contain sorted pairs with integer tag IDs

    Examples:
        >>> generate_pairs([0, 1])
        [(0, 1)]
        >>> generate_pairs([1, 2])
        [(1, 2)]
        >>> generate_pairs([1, 2, 3])
        [(1, 2), (1, 3), (2, 3)]
    """
    # Prepare an output list
    pairs = []
    # Check if it's possible to build the pairs
    if len(tag_numbers) > 1:
        # Generate all possible permutations
        pre_pairs = list(
            permutations(
                sorted(tag_numbers), 2
            )
        )
        # Remove duplicate graph edges,
        # there's no need to connect both A->B and B->A
        for pair in pre_pairs:
            pair = list(sorted(pair))
            if pair not in pairs:
                pairs.append(pair)
    # Return the list of pairs for the graph edges
    return pairs

class Pair_mgr:
    """
    This class stores tag ID pairs to build graph edges.

    Example:

        >>> from lib.graph_util import Pair_mgr
        >>> pmgr = Pair_mgr()
        >>> pmgr.push_pair((0, 1))
        >>> pmgr.push_pair((0, 1))
        >>> pmgr.push_pair((1, 2))
        >>> pmgr.get_list()
        [{'edge': ['0', '1'], 'weight': 1.0}, {'edge': ['1', '2'], 'weight': 0.5}]    

    Attributes:
        pairs (defaultdict): tag index pairs
        update_count (integer): a count of all pair updates
    """

    def __init__(self):
        # A per-pair counter
        self.pairs = defaultdict(int)
        # A full count of each pair update
        self.update_count = 0

    def push_tag_numbers(self, numbers):
        """
        Generates pairs, updates Pair_mgr with them

        Attributes:

            numbers (list): a list of integers
        """
        for pair in generate_pairs(numbers):
            self.push_pair(pair)

    def push_pair(self, pair):
        """
        Args:

            pair (tuple): a pair of tag IDs

        Example:

            >>> pmgr.push_pair((1, 2))
        """
        self.pairs[ '{} {}'.format(pair[0], pair[1]) ] += 1
        self.update_count += 1

    def get_update_count(self):
        """
        Returns:

            integer, a count of all pair updates

        Example:

            >>> pmgr = Pair_mgr()
            >>> pmgr.push_pair((0, 1))
            >>> pmgr.push_pair((0, 1))
            >>> pmgr.push_pair((1, 2))
            >>> pmgr.get_update_count()
            3
        """
        return self.update_count

    def get_edge_count(self):
        """
        Returns:

            A count of all unique graph edges

        Example:

            >>> pmgr = Pair_mgr()
            >>> pmgr.push_pair((0, 1))
            >>> pmgr.push_pair((0, 1))
            >>> pmgr.push_pair((1, 2))
            >>> pmgr.get_edge_count()
            2
        """
        return len(self.pairs.keys())

    def get_list(self):
        """
        Returns:

            A list of all graph edges with weights

        Example:

            >>> pmgr = Pair_mgr()
            >>> pmgr.push_pair((0, 1))
            >>> pmgr.push_pair((0, 1))
            >>> pmgr.push_pair((1, 2))
            >>> pmgr.get_list()
            [{'edge': ['0', '1'], 'weight': 1.0}, {'edge': ['1', '2'], 'weight': 0.5}]
        """
        # Store the count of all unique graph edges
        edge_count = self.get_edge_count()
        # Get a weighted list of the tags to iterate through
        return [
            {'edge': key.split(' '), 'weight': float(value) / edge_count}
            for key, value
            in self.pairs.items()
        ]
