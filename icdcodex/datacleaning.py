"""preprocess icd-10 hierarchy into a graphical structure that node2vec can use"""

import json
import pandas as pd
import networkx as nx
import untangle
from tqdm import tqdm


## -------- ICD 9 ------------ ##

def build_icd9_hierarchy(fp):
    """build the icd9 hierarchy

    Args:
        fp (Pathlike): Path to hierarchy spec, available at https://github.com/kshedden/icd9/blob/master/icd9/resources/icd9Hierarchy.json

    Returns:
        icd9 hierarchy (nx.Graph) and ICD9 codes (List[str])
    """
    hierarchy = pd.read_json(fp)
    G = nx.Graph()
    G.add_node("ICD")
    for chapter in hierarchy.chapter.unique():
        G.add_node(chapter)
        G.add_edge(chapter, "ICD")
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


## -------- ICD 10 CM -------- ##


def traverse_diag(G, parent, untangle_elem, extensions=None):
    """traverse the diagnosis subtrees, adding extensions as appropriate

    Diagnoses are structured in an un-intuitive way in the cms.gov XML. Seventh-
    character extensions may be specified as a child, sibling or uncle/aunt.
    Some diagnoses are non-billable because they are parents to more specific
    sub-diagnoses. Finally, 


    Args:
        G (nx.Graph): ICD hierarchy to mutate
        parent (str): parent node
        untangle_elem (untangle.Element): XML element, from untangle API
        extensions (List[Tuple[str,str]], optional): Seventh character extensions and related descriptions. Defaults to None.
    """
    self = untangle_elem.name.cdata
    desc = untangle_elem.desc.cdata
    G.add_node(self, desc=desc)
    G.add_edge(self, parent)
    try:
        extension_elems = untangle_elem.sevenChrDef.extension
    except AttributeError:
        extensions = [] if extensions is None else extensions
    else:
        extensions = [(ext["char"], ext.cdata) for ext in extension_elems]
    try:
        children = untangle_elem.diag
    except AttributeError:
        if extensions and len(self) <= 7:
            # There is an inconsistency in the XML structure where, somtimes,
            # the seventh character is specified explicitly as well as by
            # having their parent contain a <sevenChrDef> tag. In this case,
            # we simply ignore it because these codes already have a seventh
            # character
            for extension, extension_desc in extensions:
                if len(self) < 7:  # e.g. E09.37 -> E09.37X1
                    extension = "X" * (7-len(self)) + extension
                G.add_node(self+extension, desc=desc + " " + extension_desc)
                G.add_edge(self+extension, self)
    else:
        for child in children:
            traverse_diag(G, self, child, extensions)


def build_icd10_hierarchy(fp):
    """build the icd10 hierarchy

    Args:
        fp (Pathlike): Path to hierarchy spec available at https://www.cms.gov/Medicare/Coding/ICD10/Downloads/2020-ICD-10-CM-Codes.zip

    Returns:
        icd10 hierarchy (nx.Graph) and ICD10 codes (List[str])
    """
    # TODO: extract files from ZIP
    icd10_codes = []
    with open("tabular/icd10cm_codes_2021.txt") as f:
        for line in f:
            if not line.strip(): continue # blank line|
            code, *_ = line.split(" ")
            icd10_codes.append(code)
    with open("tabular/icd10cm_tabular_2021.xml") as f:
        e = untangle.parse(f)
    G = nx.Graph()
    G.add_node("ICD10CM")
    for chapter_elem in tqdm(e.ICD10CM_tabular.chapter, unit="chapter"):
        chapter = chapter_elem.desc.cdata
        G.add_node(chapter, chapter_num=chapter_elem.name.cdata)
        G.add_edge(chapter, "ICD10CM")
        for section_elem in chapter_elem.section:
            section = section_elem.desc.cdata
            try:
                diag_elems = section_elem.diag
            except AttributeError:
                """chapter collections, e.g. C00-C96 are 'Malignant neoplasms,' but those
                codes are stored in the diag Malignant neoplasms of lip, oral cavity and
                pharynx (C00-C14)"""
            else:
                G.add_node(section)
                G.add_edge(section, chapter)
                for diag_elem in diag_elems:
                    traverse(G, section, diag_elem)
    # TODO: add pruning
    return G, icd10_codes


if __name__ == "__main__":
    for build, fp_in, fp_out in [(build_icd9_hierarchy, "nbexamples/icd9Hierarchy.json", "icdcodex/data/icd9-hierarchy.json"),
                                 (build_icd10_hierarchy, "nbexamples/icd-10-cm.xml", "icdcodex/data/icd10-hierarchy.json")]:
        G, codes = build(fp_in)
        with open(fp_out, "w") as f:
            json.dump({
                "graph": nx.readwrite.json_graph.node_link_data(G),
                "codes": list(codes)
            }, f)