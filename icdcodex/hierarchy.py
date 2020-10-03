"""deserialize icd hierarchies computed in datacleaning.py"""

from typing import Optional, Sequence, Tuple
import json
from datetime import datetime
import networkx as nx
from . import data

try:
    import importlib.resources as importlib_resources
except ModuleNotFoundError:
    import importlib_resources


def icd9() -> Tuple[nx.Graph, Sequence[str]]:
    """deserialize icd9 hierarchy

    Returns:
        Tuple[nx.Graph, Sequence[str]]: ICD9 hierarchy and codes
    """
    with importlib_resources.open_text(data, "icd-9-hierarchy.json") as f:
        hierarchy = json.load(f)
    return (
        nx.readwrite.json_graph.node_link_graph(hierarchy["graph"]),
        hierarchy["codes"],
    )


def icd10cm(version: Optional[str] = None) -> Tuple[nx.Graph, Sequence[str]]:
    """deserialize icd-10-cm hierarchy

    Args:
        version (str, optional): icd-10-cm version, including 2019 to 2020. If None, use the system
            year. Defaults to None.

    Returns:
        Tuple[nx.Graph, Sequence[str]]: ICD-10-CM hierarchy and codes
    """
    if version is None:
        version = datetime.now().year
    assert version in ["2019", "2020", "2020"]
    with importlib_resources.open_text(data, f"icd-10-{version}-hierarchy.json") as f:
        hierarchy = json.loads(f.read())
    return (
        nx.readwrite.json_graph.node_link_graph(hierarchy["graph"]),
        hierarchy["codes"],
    )
