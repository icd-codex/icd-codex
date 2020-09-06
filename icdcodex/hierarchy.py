"""deserialize icd hierarchies computed in datacleaning.py"""

from typing import Sequence, Tuple
import json
import importlib
import networkx as nx


def icd9hierarchy() -> Tuple[nx.Graph, Sequence[str]]:
    """deserialize icd9 hierarchy

    Returns:
        Tuple[nx.Graph, Sequence[str]]: ICD9 hierarchy and the ICD9 codes
    """
    hierarchy = importlib.resources.open_binary('data', 'icd9-hierarchy.json')
    hierarchy = hierarchy.encode("utf-8")
    hierarchy = json.loads(hierarchy)
    return nx.readwrite.json_graph.node_link_data(hierarchy["graph"]), hierarchy["codes"]