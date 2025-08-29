# Use of DETOUR as a library

Here we provide an example to illustrate how to use DETOUR as a library. To this end we develop a test selector tool with the code pipeline provided by [SDC Testing Competition](https://github.com/christianbirchler-org/sdc-testing-competition).

# DETOUR Competition Tool for SDC Testing Competition

The competition tool that we provide uses the `select` module of `DETOUR` class from `detour` submodule. This method requires four parameters `min_select_ratio`, `max_select_ratio`, `m_closest_neighbor_count`, `w_selection_threshold`. With the specified parameters, this method selects at least `min_select_ratio` of the tests and at most `max_select_ratio` of the tests. Furthermore, the selection stops when the `m_closest_neighbor_count` closest tests of the last `w_selection_threshold` selected tests are all passing.
