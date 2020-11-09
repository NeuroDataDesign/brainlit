import pytest
from brainlit.algorithms.trace_analysis.fit_spline import GeometricGraph
import networkx as nx
import numpy as np


##############
### inputs ###
##############


def test_fit_spline_tree_invariant_bad_input():

    # test nodes must have a 'loc' attribute
    neuron_no_loc = GeometricGraph()
    neuron_no_loc.add_node(1)
    neuron_no_loc.add_node(2, loc=np.array([100, 100, 200]))
    # build spline tree using fit_spline_tree_invariant()
    with pytest.raises(KeyError, match=r"some nodes are missing the 'loc' attribute"):
        neuron_no_loc.fit_spline_tree_invariant()

    # test 'loc' attribute must be numpy.ndarray
    neuron_wrong_loc_type = GeometricGraph()
    neuron_wrong_loc_type.add_node(1, loc={})
    neuron_wrong_loc_type.add_node(2, loc=np.array([100, 100, 200]))
    with pytest.raises(
        TypeError, match=r"{} should be <class 'numpy.ndarray'>, not <class 'dict'>."
    ):
        neuron_wrong_loc_type.fit_spline_tree_invariant()

    # test 'loc' attribute must be a flat array
    neuron_nested_loc = GeometricGraph()
    neuron_nested_loc.add_node(1, loc=np.array([[]]))
    neuron_nested_loc.add_node(2, loc=np.array([100, 100, 200]))
    with pytest.raises(ValueError, match=r"nodes must be flat arrays"):
        neuron_nested_loc.fit_spline_tree_invariant()

    # test 'loc' attribute cannot be empty
    neuron_empty_loc = GeometricGraph()
    neuron_empty_loc.add_node(1, loc=np.array([]))
    neuron_empty_loc.add_node(2, loc=np.array([100, 100, 200]))
    with pytest.raises(ValueError, match=r"nodes cannot have empty 'loc' attributes"):
        neuron_empty_loc.fit_spline_tree_invariant()

    # test 'loc' attribute must be real-valued
    neuron_non_real_valued_loc = GeometricGraph()
    neuron_non_real_valued_loc.add_node(1, loc=np.array(["a"]))
    neuron_non_real_valued_loc.add_node(2, loc=np.array([100, 100, 200]))
    with pytest.raises(
        TypeError,
        match=r"\['a'\] elements should be \(<class 'numpy.integer'>, <class 'float'>\).",
    ):
        neuron_non_real_valued_loc.fit_spline_tree_invariant()

    # test 'loc' attribute must have 3 coordinates
    neuron_wrong_coordinates = GeometricGraph()
    neuron_wrong_coordinates.add_node(1, loc=np.array([1, 2]))
    neuron_wrong_coordinates.add_node(2, loc=np.array([100, 100, 200]))
    with pytest.raises(ValueError, match=r"'loc' attributes must contain 3 coordinate"):
        neuron_wrong_coordinates.fit_spline_tree_invariant()

    # test 'loc' attributes must be unique
    neuron_duplicate_loc = GeometricGraph()
    neuron_duplicate_loc.add_node(1, loc=np.array([100, 100, 200]))
    neuron_duplicate_loc.add_node(2, loc=np.array([100, 100, 200]))
    with pytest.raises(ValueError, match=r"there are duplicate nodes"):
        neuron_duplicate_loc.fit_spline_tree_invariant()

    # test edges must be a valid cover of the graph
    neuron_no_edges = GeometricGraph()
    neuron_no_edges.add_node(1, loc=np.array([100, 100, 200]))
    neuron_no_edges.add_node(2, loc=np.array([200, 200, 400]))
    with pytest.raises(
        ValueError, match=r"the edges are not a valid cover of the graph"
    ):
        neuron_no_edges.fit_spline_tree_invariant()

    # test there cannot be undirected cycles in the graph
    neuron_cycles = GeometricGraph()
    neuron_cycles.add_node(1, loc=np.array([100, 100, 200]))
    neuron_cycles.add_node(2, loc=np.array([200, 0, 200]))
    neuron_cycles.add_node(3, loc=np.array([200, 300, 200]))
    neuron_cycles.add_node(4, loc=np.array([300, 400, 200]))
    neuron_cycles.add_node(5, loc=np.array([100, 500, 200]))
    # add edges
    neuron_cycles.add_edge(2, 1)
    neuron_cycles.add_edge(3, 2)
    neuron_cycles.add_edge(4, 3)
    neuron_cycles.add_edge(5, 4)
    neuron_cycles.add_edge(3, 5)
    with pytest.raises(ValueError, match=r"the graph contains undirected cycles"):
        neuron_cycles.fit_spline_tree_invariant()

    # test there cannot be disconnected segments in the graph
    neuron_disconnected_segments = GeometricGraph()
    neuron_disconnected_segments.add_node(1, loc=np.array([100, 100, 200]))
    neuron_disconnected_segments.add_node(2, loc=np.array([200, 0, 200]))
    neuron_disconnected_segments.add_node(3, loc=np.array([200, 300, 200]))
    neuron_disconnected_segments.add_node(4, loc=np.array([300, 400, 200]))
    neuron_disconnected_segments.add_node(5, loc=np.array([100, 500, 200]))
    # add edges
    neuron_disconnected_segments.add_edge(2, 1)
    neuron_disconnected_segments.add_edge(3, 4)
    neuron_disconnected_segments.add_edge(3, 5)
    # build spline tree using fit_spline_tree_invariant()
    with pytest.raises(ValueError, match=r"the graph contains disconnected segments"):
        neuron_disconnected_segments.fit_spline_tree_invariant()


##################
### validation ###
##################


# def test_splNum():
#     """check resultant number of splines"""

#     neuron = GeometricGraph()
#     # add nodes
#     neuron.add_node(1, loc=np.array([100, 100, 200]))
#     neuron.add_node(2, loc=np.array([200, 0, 200]))
#     neuron.add_node(3, loc=np.array([200, 300, 200]))
#     neuron.add_node(4, loc=np.array([300, 400, 200]))
#     neuron.add_node(5, loc=np.array([100, 500, 200]))
#     # define soma
#     soma = [100, 100, 200]
#     # add edges
#     neuron.add_edge(2, 1)
#     neuron.add_edge(2, 3)
#     neuron.add_edge(3, 4)
#     neuron.add_edge(3, 5)
#     spline_tree = neuron.fit_spline_tree_invariant()
#     # expect to have 2 splines
#     if len(spline_tree.nodes) != 2:
#         raise ValueError("The total number of splines is incorrect.")
