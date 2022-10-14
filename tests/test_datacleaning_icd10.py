import pytest
import untangle
from icdcodex import hierarchy, datacleaning


@pytest.mark.parametrize("hierarchy,codes", [
    hierarchy.icd10cm("2019"),
    hierarchy.icd10cm("2020"),
    hierarchy.icd10cm("2021"),
    hierarchy.icd10cm("2022"),
])
class TestAllRevisionsOfICD10CM:

    @pytest.mark.unit
    @pytest.mark.parametrize("extension", ["A", "D", "S"])
    def test_T07(self, hierarchy, codes, extension):
        """T07 has the unique structure that only its section is defined
        along with an extension code"""
        T07 = f"T07.XXX{extension}"
        assert T07 in codes
        assert T07 in hierarchy.nodes()

    @pytest.mark.unit
    def test_a_super_chapter_not_included(self, hierarchy, codes):
        assert "C00-C96" not in hierarchy.nodes()

    @pytest.mark.unit
    def test_a_normal_chapter_included(self, hierarchy, codes):
        assert "Malignant neoplasms of lip, oral cavity and pharynx (C00-C14)" in hierarchy.nodes()


@pytest.mark.xfail
@pytest.mark.unit
def test_extension_added_from_uncle():
    raise NotImplementedError


sibling_xml = """\
<ICD10CM.tabular>
    <chapter>
        <name>4</name>
        <desc>Endocrine, nutritional and metabolic diseases (E00-E89)</desc>
        <section id="E08-E13">
            <desc>Diabetes mellitus (E08-E13)</desc>
            <diag>
                <name>E10</name>
                <desc>Type 1 diabetes mellitus</desc>
                <diag>
                    <name>E10.32</name>
                    <desc>Type 1 diabetes mellitus with mild nonproliferative diabetic retinopathy</desc>
                    <sevenChrDef>
                        <extension char="1">right eye</extension>
                        <extension char="2">left eye</extension>
                        <extension char="3">bilateral</extension>
                        <extension char="9">unspecified eye</extension>
                    </sevenChrDef>
                    <diag>
                        <name>E10.321</name>
                        <desc>Type 1 diabetes mellitus with mild nonproliferative diabetic retinopathy with macular edema</desc>
                    </diag>
                </diag>
            </diag>
        </section>
    </chapter>
</ICD10CM.tabular>"""
@pytest.mark.unit
@pytest.mark.filterwarnings("ignore: parsing strangeness")  # this happens when root node has a single child
def test_extension_added_from_sibling():
    codes_expected = ["E10.3211", "E10.3212", "E10.3213", "E10.3219"]
    e = untangle.parse(sibling_xml)
    H, _ = datacleaning.build_icd10_hierarchy(e, codes_expected, "root", prune_extra_codes=False)
    leafs = [n for n in H.nodes() if H.degree[n] == 1 and n != "root"]
    assert leafs
    for leaf in leafs:
        assert leaf in codes_expected


@pytest.mark.xfail
@pytest.mark.unit
def test_extension_added_from_child():
    raise NotImplementedError


def test_only_certain_codes_pruned_after_building_hierarchy(hierarchy_construction_intermediates):
    """Due to the following note, we add after the fact pruning:

    7th characters D and S do not apply to codes in category S06 with 6th
    character 7 - death due to brain injury prior to regaining consciousness,
    or 8 - death due to other cause prior to regaining consciousness.
    """
    _, untangle_elem, codes = hierarchy_construction_intermediates
    codes = set(codes)
    H, _ = datacleaning.build_icd10_hierarchy(untangle_elem, codes, prune_extra_codes=False)
    leaf_nodes = [n for n in H.nodes() if H.degree[n] == 1]
    leaf_nodes_that_would_otherwise_be_pruned = {leaf for leaf in leaf_nodes if leaf not in codes}
    assert leaf_nodes_that_would_otherwise_be_pruned == {
        'S06.1X7D', 'S06.1X7S', 'S06.1X8D', 'S06.1X8S', 'S06.2X7D', 'S06.2X7S',
        'S06.2X8D', 'S06.2X8S', 'S06.307D', 'S06.307S', 'S06.308D', 'S06.308S',
        'S06.317D', 'S06.317S', 'S06.318D', 'S06.318S', 'S06.327D', 'S06.327S',
        'S06.328D', 'S06.328S', 'S06.337D', 'S06.337S', 'S06.338D', 'S06.338S',
        'S06.347D', 'S06.347S', 'S06.348D', 'S06.348S', 'S06.357D', 'S06.357S',
        'S06.358D', 'S06.358S', 'S06.367D', 'S06.367S', 'S06.368D', 'S06.368S',
        'S06.377D', 'S06.377S', 'S06.378D', 'S06.378S', 'S06.387D', 'S06.387S',
        'S06.388D', 'S06.388S', 'S06.4X7D', 'S06.4X7S', 'S06.4X8D', 'S06.4X8S',
        'S06.5X7D', 'S06.5X7S', 'S06.5X8D', 'S06.5X8S', 'S06.6X7D', 'S06.6X7S',
        'S06.6X8D', 'S06.6X8S', 'S06.817D', 'S06.817S', 'S06.818D', 'S06.818S',
        'S06.827D', 'S06.827S', 'S06.828D', 'S06.828S', 'S06.897D', 'S06.897S',
        'S06.898D', 'S06.898S', 'S06.9X7D', 'S06.9X7S', 'S06.9X8D', 'S06.9X8S'
    }


@pytest.mark.parametrize("root_name", ["root", "r00t", -1, float("inf")])
def test_root_node_can_be_renamed(root_name, hierarchy_construction_intermediates):
    _, untangle_elem, codes = hierarchy_construction_intermediates
    H, _ = datacleaning.build_icd10_hierarchy(untangle_elem, codes, root_name=root_name)
    assert root_name in H.nodes()