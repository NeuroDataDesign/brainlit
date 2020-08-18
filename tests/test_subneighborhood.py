import pytest
from brainlit.utils.session import NeuroglancerSession
from brainlit.feature_extraction import neighborhood as nbrhood
import numpy as np
import pandas as pd
from cloudvolume import CloudVolume

from pathlib import Path

URL = (Path(__file__).resolve().parents[1] / "data" / "upload").as_uri()
# URL = "s3://mouse-light-viz/precomputed_volumes/brain1"
SIZE = 2
OFF = [15, 15, 15]


@pytest.fixture
def gen_array():
    nbr = nbrhood.NeighborhoodFeatures(
        url=URL, size=SIZE, offset=[15, 15, 15], segment_url=URL + "_segments"
    )
    df_nbr = nbr.fit([2], 5)
    ind = SIZE * 2 + 1
    arr = df_nbr.iloc[2, 3:].values.reshape((ind, ind, ind))
    return arr


##############
### inputs ###
##############


def test_subneighborhood_bad_inputs(gen_array):
    arr = gen_array
    arr_flat = arr.flatten()
    with pytest.raises(TypeError):
        nbrhood.subsample("asdf", (5, 5), (3, 3))
    # 2d
    with pytest.raises(TypeError):
        nbrhood.subsample(arr_flat, 0, (3, 3))
    with pytest.raises(ValueError):
        nbrhood.subsample(arr_flat, (5), (3, 3))
    with pytest.raises(TypeError):
        nbrhood.subsample(arr_flat, (-1, -1), (3, 3))
    with pytest.raises(TypeError):
        nbrhood.subsample(arr_flat, (5, 5), 0)
    with pytest.raises(ValueError):
        nbrhood.subsample(arr_flat, (5, 5), (3))
    with pytest.raises(ValueError):
        nbrhood.subsample(arr_flat, (5, 5), (-1, -1))
    # 3d
    with pytest.raises(TypeError):
        nbrhood.subsample(arr_flat, 0, (3, 3, 3))
    with pytest.raises(ValueError):
        nbrhood.subsample(arr_flat, (5), (3, 3, 3))
    with pytest.raises(ValueError):
        nbrhood.subsample(arr_flat, (-1, -1, -1), (3, 3, 3))
    with pytest.raises(TypeError):
        nbrhood.subsample(arr_flat, (5, 5, 5), 0)
    with pytest.raises(ValueError):
        nbrhood.subsample(arr_flat, (5, 5, 5), (3))
    with pytest.raises(ValueError):
        nbrhood.subsample(arr_flat, (5, 5, 5), (-1, -1, -1))


##################
### validation ###
##################


def test_2d(gen_array):
    arr = gen_array
    a1 = arr[2, :, :].flatten()
    sub_a1 = nbrhood.subsample(a1, (5, 5), (3, 3)).reshape((3, 3))
    assert np.array_equal(sub_a1, arr[2, 1:4, 1:4])


def test_even(gen_array):
    arr = gen_array
    a1 = arr[2, :, :].flatten()
    sub_a1_even = nbrhood.subsample(a1, (5, 5), (4, 4)).reshape((4, 4))
    assert np.array_equal(sub_a1_even, arr[2, 0:4, 0:4])


def test_3d(gen_array):
    arr = gen_array
    a2 = arr.flatten()
    sub_a2 = nbrhood.subsample(a2, (5, 5, 5), (3, 3, 3)).reshape((3, 3, 3))
    assert np.array_equal(sub_a2, arr[1:4, 1:4, 1:4])
