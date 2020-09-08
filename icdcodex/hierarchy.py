"""deserialize icd hierarchies computed in datacleaning.py"""

from typing import Sequence, Tuple
import json
import importlib
import networkx as nx
from . import data

def icd9hierarchy() -> Tuple[nx.Graph, Sequence[str]]:
    """deserialize icd9 hierarchy

    Returns:
        Tuple[nx.Graph, Sequence[str]]: ICD9 hierarchy and the ICD9 codes
    """
    with importlib.resources.open_binary(data, 'icd9hierarchy.json') as f:
        hierarchy = f.read().decode("utf-8")
        hierarchy = json.loads(hierarchy)
    return nx.readwrite.json_graph.node_link_graph(hierarchy["graph"]), hierarchy["codes"]