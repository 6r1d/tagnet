"""
This module contains functions to perform drawing using NetworkX.
"""

from networkx import spring_layout, draw, draw_networkx_edges, draw_networkx_nodes, draw_networkx_labels
import matplotlib.pyplot as plt

def plot_graph(G):
    """
    Plots a NetworkX graph.

    Arguments:

        G: a NetworkX graph instance
    """
    # Prepare a graph layout
    pos = spring_layout(G)
    # Add graph edges
    edges = [(u, v) for (u, v, d) in G.edges(data=True)]
    # Configure a graph style
    draw_networkx_edges(G, pos, edgelist=edges, width=1)
    draw_networkx_nodes(G, pos, node_size=250)
    draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")
    # Display a plotted graph
    plt.axis("off")
    plt.show()

def plot_graph_basic(G):
    """
    Plots a NetworkX graph (a basic version).

    Arguments:

        G: a NetworkX graph instance
    """
    draw(G)
    plt.show()

def export_graph(G, name):
    """
    Plots a NetworkX graph (a basic version).

    Example:

        >>> export_graph(G, "tags.png")

    Arguments:

        G: a NetworkX graph instance
        name (str): a graph name
    """
    draw(G)
    plt.savefig(name)
