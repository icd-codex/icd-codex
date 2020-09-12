"""deserialize icd hierarchies computed in datacleaning.py"""

from typing import Literal, Optional, Sequence, Tuple
import json
import importlib
from datetime import datetime
import networkx as nx
from . import data


def icd9() -> Tuple[nx.Graph, Sequence[str]]:
    """deserialize icd9 hierarchy

    Returns:
        Tuple[nx.Graph, Sequence[str]]: ICD9 hierarchy and codes
    """
    with importlib.resources.open_binary(data, "icd-9-hierarchy.json") as f:
        hierarchy = f.read().decode("utf-8")
        hierarchy = json.loads(hierarchy)
    return (
        nx.readwrite.json_graph.node_link_graph(hierarchy["graph"]),
        hierarchy["codes"],
    )


def icd10cm(
    version: Optional[Literal["2019", "2020", "2020"]] = None
) -> Tuple[nx.Graph, Sequence[str]]:
    """deserialize icd-10-cm hierarchy

    Args:
        version (str, optional): icd-10-cm version, including 2019 to 2020. If None, use the system
            year. Defaults to None.

    Returns:
        Tuple[nx.Graph, Sequence[str]]: ICD-10-CM hierarchy and codes
    """
    if version is None:
        version = datetime.now().year
    with importlib.resources.open_binary(data, f"icd-10-{version}-hierarchy.json") as f:
        hierarchy = f.read().decode("utf-8")
        hierarchy = json.loads(hierarchy)
    return (
        nx.readwrite.json_graph.node_link_graph(hierarchy["graph"]),
        hierarchy["codes"],
    )
