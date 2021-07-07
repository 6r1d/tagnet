"""
Contains an entry-point function to.
Provided the command-line arguments, it can:

* Sort and filter CLIP tags
* Display tags as a NetworkX graph
* Export a NetworkX graph as JSON
"""

# Required by tag counter
import operator as op
# Required by tag counter and graph builder
from lib.prompts import load_prompts
from lib.tags import extract_tags, Tag_processor
# Required by graph builder
from lib.graph_util import Pair_mgr, build_graph
from lib.plot import plot_graph, plot_graph_basic
# Required by graph export tool
from networkx.readwrite import json_graph
from json import dump

OPERATORS = {
    '>': op.gt,
    '<': op.lt,
    '>=': op.ge,
    '<=': op.le,
    '=': op.eq
}

def process_dir(args):
    """
    An entry-point function.

    Attributes:

        args (argparse.Namespace): an object containing the parsed argumentss
    """
    # Initialize a tag processor
    tp = Tag_processor()
    # Initialize a pair manager
    pmgr = Pair_mgr() if args.mode in ['display_graph', 'export_graph'] else None
    # Prompts to scan
    prompts = load_prompts(args.path)
    # Iterate all available prompts
    for prompt in prompts:
        # Extract a list of tags
        tags = extract_tags(prompt)
        if args.mode in ['display_graph', 'export_graph']:
            # Add tags to Tag_processor,
            # get number for each added tag
            tag_numbers = tp.put_tags(tags)
            # Update the Pair_mgr
            pmgr.push_tag_numbers(tag_numbers)
        else:
            # Add tags to the Tag_processor
            tp.add_tags(tags)
    if args.mode in ['display_graph', 'export_graph']:
        # Build a NetworkX graph
        G = build_graph(tp, pmgr)
    elif args.mode == 'count_tags':
        if 'filter' in args and args.filter is not None and 'condition' in args.filter:
            operator = OPERATORS[args.filter['condition']]
        else:
            operator = None
        # Display the tags and how often those are used
        for key, value in tp.get_tag_numbers():
            if operator is None or operator(int(value), args.filter['number']):
                print('{} | {}'.format(key, value))
    if args.mode == 'display_graph':
        # Plot and display a graph
        plot_graph_basic(G)
    if args.mode == 'export_graph':
        # Create node data for a graph
        node_link_data = json_graph.node_link_data(G)
        node_link_data['nodes'] = [node for node in node_link_data['nodes'] if 'name' in node]
        # TODO check it's possible to create a file
        dump(node_link_data, args.output_file, indent=4, ensure_ascii=False)
