"""preprocess icd-10 hierarchy into a graphical structure that node2vec can use"""

import xmltodict
import pandas as pd
import networkx as nx


def icd9hierarchy(fp):
    hierarchy = pd.read_json(fp)
    G = nx.Graph()
    G.add_node("root")
    for chapter in hierarchy.chapter.unique():
        G.add_node(chapter)
        G.add_edge(chapter, "root")
    G.add_nodes_from(hierarchy.subchapter.unique())
    for chapter, child_df in hierarchy.groupby("chapter"):
        if chapter in ['Diseases Of The Blood And Blood-Forming Organs', 'Congenital Anomalies']:
            # no sub-chapters
            continue
        for subchapter in child_df.subchapter.unique():
            G.add_node(subchapter)
            G.add_edge(chapter, subchapter)
    icd_codes_with_subchapters = hierarchy.subchapter.isna()
    for parent_prop, child_prop, df in [
        ("chapter", "major", hierarchy[~icd_codes_with_subchapters]),
        ("subchapter", "major", hierarchy[icd_codes_with_subchapters]),
        ("major", "icd9", hierarchy)]:
        for parent, child_df in df.groupby(parent_prop):
            for child in child_df[child_prop].unique():
                G.add_node(str(child))
                G.add_edge(str(child), str(parent))
    icd_codes = hierarchy.icd9.unique()
    assert not any(code for code in icd_codes if code not in G.nodes()), \
        f"some codes are not represented in the networkx hierarchy!"
    return G, icd_codes


def icd10hierarchy(fp) -> nx.Graph:
    with open(fp) as fd:
        doc = xmltodict.parse(fd.read())
    j = doc["ICD10CM.tabular"]["chapter"]
    G = nx.Graph()
    G.add_node("ICD")  #  <- potentially remove
    for chapter in range(len(j)):
        for section in range(len(j[chapter])):
            section = str(section)
            G.add_node(section)
            G.add_edge("ICD", section)  #  <- potentially remove
            try:
                for diag in range(len(j[chapter]["section"][section])):
                    G.add_node(x := j[chapter]["section"][section]["@id"])
                    G.add_edge(section, x)
                    try:
                        for diag_2 in range(len(j[chapter]["section"][section]["diag"][diag])):
                            G.add_node(x := str(j[chapter]["section"][section]["diag"][diag]["name"]))
                            G.add_edge(j[chapter]["section"][section]["@id"], x)
                            try:
                                G.add_node(y := j[chapter]["section"][section]["diag"][diag]["diag"][diag_2]["name"])
                                G.add_edge(x, y)
                            except (KeyError, IndexError):
                                break
                    except (KeyError, IndexError):
                        break
            except (KeyError, IndexError):
                break
    G.remove_nodes_from(nx.isolates(G))
    return G
