Plans
=====

Modes
-----

Currently, there's two modes to display the graph: Python's WxWidgets interface and a web interface.

There exists a potential to get more information out of the dataset by expanding available modes.

Community detection
^^^^^^^^^^^^^^^^^^^

I should try several community detection [#f1]_ [#f2]_ methods.

Adjacency graph
^^^^^^^^^^^^^^^

A mode for an adjacency graph will require a bit more work, for example,
exporting only a top N tags and limit tag lengths so everything can be displayed.

* `StackOverflow <https://stackoverflow.com/>`_: `Method to save networkx graph to json graph? <https://stackoverflow.com/questions/3162909/>`_
* `NetworkX <https://networkx.org/>`_: `Reading and writing graphs » JSON <https://networkx.org/documentation/stable/reference/readwrite/json_graph.html>`_

Word2Vec
^^^^^^^^

I am not sure if it can be used as-is, but there were some works that remind me it can be useful to try later. [#f3]_ [#f4]_

Experiments
-----------

Edge weighting
^^^^^^^^^^^^^^

Edge weights in pair_mgr are currently divided by an :code:`edge_count` parameter.
I am not sure it is an ideal option that allows to see the maximum amount of details.

Weighting by relation
^^^^^^^^^^^^^^^^^^^^^

* Will add edges between tags like :code:`Abstract style` and :code:`Abstract` add more context?
* How to weight those edges properly?

Argparse
--------

* Save contents for :code:`tag_manager` and :code:`pair_manager`

-------------------

.. rubric:: Footnotes

.. [#f1] `Understanding Community Detection Algorithms with Python NetworkX <https://memgraph.com/blog/community_detection-algorithms_with_python_networkx>`_
.. [#f2] `Louvain <https://python-louvain.readthedocs.io/en/latest/index.html>`_
.. [#f3] `Node2vec <https://snap.stanford.edu/node2vec/>`_: Scalable Feature Learning for Networks; `How node2vec works <https://www.freecodecamp.org/news/how-to-think-about-your-data-in-a-different-way-b84306fc2e1d/>`_ — and what it can do that word2vec can’t
.. [#f4] `Paper2vec <https://arxiv.org/abs/1703.06587>`_: Citation-Context Based Document Distributed Representation for Scholar Recommendation by Han Tian and Hankz Hankui Zhuo

