"""preprocess icd-10 hierarchy into a graphical structure that node2vec can use"""

import xmltodict
import networkx as nx


def icd10hierarchy(fp) -> nx.Graph:
    with open(fp) as fd:
        doc = xmltodict.parse(fd.read())
    j = doc["ICD10CM.tabular"]["chapter"]
    G = nx.Graph()
    G.add_node("ICD")  #  <- potentially remove
    for chapter in range(len(j)):
        for section in range(len(j[chapter])):
            G.add_node(section)
            G.add_edge("ICD", section)  #  <- potentially remove
            try:
                for diag in range(len(j[chapter]["section"][section])):
                    G.add_node(j[chapter]["section"][section]["@id"])
                    G.add_edge(section, j[chapter]["section"][section]["@id"])
                    try:
                        for diag_2 in range(len(j[chapter]["section"][section]["diag"][diag])):
                            G.add_node(
                                j[chapter]["section"][section]["diag"][diag]["name"]
                            )
                            G.add_edge(
                                j[chapter]["section"][section]["@id"],
                                j[chapter]["section"][section]["diag"][diag]["name"],
                            )
                            try:
                                x = j[chapter]["section"][section]["diag"][diag]["diag"][diag_2]["name"]
                                G.add_node(x)
                                G.add_edge(
                                    j[chapter]["section"][section]["diag"][diag]["name"],
                                    x,
                                )
                            except (KeyError, IndexError):
                                break
                    except (KeyError, IndexError):
                        break
            except (KeyError, IndexError):
                break
    G.remove_nodes_from(nx.isolates(G))
    return G
