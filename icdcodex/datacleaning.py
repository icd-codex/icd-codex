"""preprocess icd-10 hierarchy into a graphical structure that node2vec can use"""


from typing import List, Optional
import warnings
import tempfile
import re
import json
from zipfile import ZipFile
from pathlib import Path
import requests
import untangle
import pandas as pd
import networkx as nx


def main():
    G_icd9, codes_icd9 = build_icd9_hierarchy_from_url(
        "https://raw.githubusercontent.com/kshedden/icd9/master/icd9/resources/icd9Hierarchy.json"
    )
    G_icd10cm_2019, codes_icd10cm_2019 = build_icd10_hierarchy_from_url(
        "https://www.cms.gov/Medicare/Coding/ICD10/Downloads/2019-ICD-10-CM-Code-Descriptions.zip",
        "https://www.cms.gov/Medicare/Coding/ICD10/Downloads/2019-ICD-10-CM-Tables-and-Index.zip",
    )
    G_icd10cm_2020, codes_icd10cm_2020 = build_icd10_hierarchy_from_url(
        "https://www.cms.gov/Medicare/Coding/ICD10/Downloads/2020-ICD-10-CM-Codes.zip",
        "https://www.cms.gov/Medicare/Coding/ICD10/Downloads/2020-ICD-10-CM-Code-Tables.zip",
    )
    G_icd10cm_2021, codes_icd10cm_2021 = build_icd10_hierarchy_from_url(
        "https://www.cms.gov/files/zip/2021-code-descriptions-tabular-order.zip",
        "https://www.cms.gov/files/zip/2021-code-tables-and-index.zip",
    )
    outdir = Path("icdcodex/data")
    for G, codes, fname in [
        (G_icd9, codes_icd9, "icd-9-hierarchy.json"),
        (G_icd10cm_2019, codes_icd10cm_2019, "icd-10-2019-hierarchy.json",),
        (G_icd10cm_2020, codes_icd10cm_2020, "icd-10-2020-hierarchy.json",),
        (G_icd10cm_2021, codes_icd10cm_2021, "icd-10-2021-hierarchy.json",),
    ]:
        with open(outdir / fname, "w") as f:
            root_node, *_ = nx.topological_sort(G)
            j = {
                "tree": nx.readwrite.json_graph.tree_data(G, root_node),
                "codes": sorted(codes),
            }
            json.dump(j, f)


# -------- ICD 9 ------------ #


def build_icd9_hierarchy_from_url(
    url="https://github.com/kshedden/icd9/blob/master/icd9/resources/icd9Hierarchy.json",
    root_name=None
):
    """build the icd9 hierarchy by downloading the hierarchy files

    Args:
        url (str, optional): url to hierarchy spec. Defaults to "https://github.com/kshedden/icd9/blob/master/icd9/resources/icd9Hierarchy.json".
        root_name (str, option): arbitrary name for the root of the hierarchy. Defaults to "root."

    Returns:
        icd-9 hierarchy (nx.Graph) and ICD9 codes (List[str])
    """
    with tempfile.NamedTemporaryFile("wt") as f:
        f.write(requests.get(url).content.decode())
        f.seek(0)
        return build_icd9_hierarchy(f.name)


def build_icd9_hierarchy(fp, root_name=None):
    """build the icd9 hierarchy

    Args:
        fp (Pathlike): Path to hierarchy spec, available at https://github.com/kshedden/icd9/blob/master/icd9/resources/icd9Hierarchy.json
        root_name (str, option): arbitrary name for the root of the hierarchy. Defaults to "root."

    Returns:
        icd-9 hierarchy (nx.Graph) and ICD9 codes (List[str])
    """
    if root_name is None:
        root_name = "root"
    hierarchy = pd.read_json(fp)
    G = nx.DiGraph()
    G.add_node(root_name)
    for chapter in hierarchy.chapter.unique():
        G.add_edge(root_name, chapter)
    G.add_nodes_from(hierarchy.subchapter.unique())
    for chapter, child_df in hierarchy.groupby("chapter"):
        if chapter in [
            "Diseases Of The Blood And Blood-Forming Organs",
            "Congenital Anomalies",
        ]:
            # no sub-chapters
            continue
        for subchapter in child_df.subchapter.unique():
            G.add_edge(chapter, subchapter)
    icd_codes_with_subchapters = ~hierarchy.subchapter.isna()
    for parent_prop, child_prop, df in [
        ("chapter", "major", hierarchy[~icd_codes_with_subchapters]),
        ("subchapter", "major", hierarchy[icd_codes_with_subchapters]),
    ]:
        for parent, child_df in df.groupby(parent_prop):
            for child in child_df[child_prop].unique():
                G.add_edge(str(parent), str(child))
    icd9_descriptions = {}
    for parent, icd_df in hierarchy.groupby("major"):
        for _, icd in icd_df.iterrows():
            icd9_descriptions[icd.icd9] = {"description": icd.descLong}
            G.add_edge(str(parent), icd.icd9)
    icd_codes = hierarchy.icd9.unique()
    assert not any(
        code for code in icd_codes if code not in G.nodes()
    ), "some codes are not represented in the networkx hierarchy!"
    G = nx.algorithms.traversal.breadth_first_search.bfs_tree(G, source=root_name)
    nx.set_node_attributes(G, icd9_descriptions)
    return G, icd_codes


# -------- ICD 10 CM -------- #


def build_icd10_hierarchy_from_url(
    code_desc_url, code_table_url, root_name: Optional[str] = None, return_intermediates = False
):
    """build the icd10 hierarchy by downloading from cms.gov

    Args:
        code_desc_url (str): url to the "Code Descriptions in Tabular Order (ZIP)" file
        code_table_url (str): url to the "Code Tables and Index (ZIP)" file
        root_name (str, option): arbitrary name for the root of the hierarchy. Defaults to "root."
        return_intermediates (bool): If True, return the untangle element and codes. Defaults to False.

    Returns:
        Tuple[nx.Graph, List[str]]: icd10 hierarchy and ICD-10-CM codes
    """
    with tempfile.NamedTemporaryFile("wb") as desc_f, tempfile.NamedTemporaryFile(
        "wb"
    ) as table_f:
        desc_f.write(requests.get(code_desc_url).content)
        desc_f.seek(0)
        table_f.write(requests.get(code_table_url).content)
        table_f.seek(0)
        return build_icd10cm_hierarchy_from_zip(desc_f.name, table_f.name, root_name, return_intermediates)


def build_icd10cm_hierarchy_from_zip(
    code_desc_zip_fp, code_table_zip_fp, root_name: Optional[str] = None, return_intermediates = False
):
    """build the icd10 hierarchy from zip files downloaded from cms.gov

    Args:
        code_desc_zip_fp (Pathlike): file path to the "Code Descriptions in Tabular Order (ZIP)" file
        code_table_zip_fp ([type]): file path to the "Code Tables and Index (ZIP)" file
        root_name (str, option): arbitrary name for the root of the hierarchy. Defaults to "root."
        return_intermediates (bool): If True, return the untangle element and codes. Defaults to False.

    Returns:
        Tuple[nx.Graph, List[str]]: icd10 hierarchy and ICD-10-CM codes
    """
    codes = []
    with ZipFile(code_desc_zip_fp) as z:
        (code_desc_fp,) = [
            n for n in z.namelist() if re.findall(r"icd10cm_codes_\d{4}\.txt$", n)
        ]
        with z.open(code_desc_fp, "r") as f:
            for line in f:
                if not line.strip():
                    continue  # blank line
                code, *_ = line.decode().split(" ")
                if 3 < len(code) and "." not in code:
                    code = "{}.{}".format(code[:3], code[3:])
                codes.append(code)
    with ZipFile(code_table_zip_fp) as z:
        (code_table_fp,) = [
            n for n in z.namelist() if re.findall(r"icd10cm_tabular_\d{4}\.xml$", n)
        ]
        with z.open(code_table_fp, "r") as f:
            e = untangle.parse(f)
    if return_intermediates:
        return build_icd10_hierarchy(e, codes, root_name), e, codes
    return build_icd10_hierarchy(e, codes, root_name)


def build_icd10_hierarchy(
    xml_root: untangle.Element,
    codes: List[str],
    root_name: Optional[str] = None,
    prune_extra_codes: bool = True,
):
    """build the icd10 hierarchy

    Some codes are specified to be invalid by plain text, so they are
    pruned by comparing them to a specified set of codes.

    Args:
        xml_root (untangle.Element): root element of the code table XML
        codes (List[str]): list of ICD codes
        root_name (str, option): arbitrary name for the root of the hierarchy. Defaults to "root."
        prune_extra_codes (bool): If True, remove any leaf node not specified in `codes`
    Returns:
        Tuple[nx.Graph, List[str]]: icd10 hierarchy and ICD-10-CM codes
    """
    if root_name is None:
        root_name = "root"
    G = nx.Graph()
    G.add_node(root_name)
    for chapter_elem in xml_root.ICD10CM_tabular.chapter:
        chapter = chapter_elem.desc.cdata
        G.add_node(chapter, chapter_num=chapter_elem.name.cdata)
        G.add_edge(chapter, root_name)
        for section_elem in chapter_elem.section:
            section = section_elem.desc.cdata
            try:
                diag_elems = section_elem.diag
            except AttributeError:
                pass  # e.g., "C00-C96" has no codes but "C00-C14" does
            else:
                G.add_node(section)
                G.add_edge(section, chapter)
                for diag_elem in diag_elems:
                    traverse_diag(G, section, diag_elem)
    leafs = [n for n in G.nodes() if G.degree[n] == 1]
    if root_name in leafs:
        warnings.warn(UserWarning(f"parsing strangeness, root node `{root_name}` is a leaf"))
    if prune_extra_codes:
        codes_ = set(codes)
        G.remove_nodes_from(leaf for leaf in leafs if leaf not in codes_)
    G = nx.algorithms.traversal.breadth_first_search.bfs_tree(G, source=root_name)
    return G, codes


def traverse_diag(G, parent, untangle_elem, extensions=None):
    """traverse the diagnosis subtrees, adding extensions as appropriate

    Seventh-character extensions may be specified as a child, sibling or
    uncle/aunt. Also, some diagnoses are non-billable because they are,
    parents to more specific sub-diagnoses.

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
        if extensions:
            if 7 < len(self):
                # There is an inconsistency in the XML structure where, somtimes,
                # the seventh character is specified explicitly as well as by
                # having their parent contain a <sevenChrDef> tag. In this case,
                # we simply ignore it because these codes already have a seventh
                # character
                return
            for extension, extension_desc in extensions:
                if "." not in self:  # e.g., T07 -> T07.XXXD
                    num_xs_needed = 7 - len(self) - len(extension)
                    extension = "." + ("X" * num_xs_needed) + extension
                else:  # e.g. E09.37 -> E09.37X1
                    num_xs_needed = 8 - len(self) - len(extension)
                    extension = ("X" * num_xs_needed) + extension
                G.add_node(self + extension, desc=desc + " " + extension_desc)
                G.add_edge(self + extension, self)
    else:
        for child in children:
            traverse_diag(G, self, child, extensions)


if __name__ == "__main__":
    main()
