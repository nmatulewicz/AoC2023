import pytest
from day_5.solution_part_2 import MapFunc, Range, RangeMapper, SortedRangeList



@pytest.mark.parametrize("source_ranges, expected_result", [
    (SortedRangeList([Range(5, 10)]), SortedRangeList([Range(7, 12)])),
    (SortedRangeList([Range(-3, 4)]), SortedRangeList([Range(-3, 4)])),
    (SortedRangeList([Range(400, 1000)]), SortedRangeList([Range(400, 1000)])),
    (SortedRangeList([Range(31, 37)]), SortedRangeList([Range(26, 27), Range(31, 31), Range(34, 37)])),
    (SortedRangeList([Range(3, 5)]), SortedRangeList([Range(3, 4), Range(7, 7)])),
    (SortedRangeList([Range(6, 24)]), SortedRangeList([Range(8, 14), Range(21, 27)])),
    (SortedRangeList([Range(6, 24), Range(30, 31)]),
     SortedRangeList([Range(8, 14), Range(21, 27), Range(29, 29), Range(31, 31)])),
])
def test_range_mapper_map(source_ranges, expected_result):
    # arrange
    sorted_map_funcs = [
        MapFunc(Range(5, 10), delta=2),
        MapFunc(Range(15, 20), delta=7),
        MapFunc(Range(25, 30), delta=-1),
        MapFunc(Range(32, 33), delta=-6),
    ]
    range_mapper = RangeMapper(sorted_map_funcs)

    # act
    result = range_mapper.map(source_ranges)

    # assert
    assert result == expected_result


@pytest.mark.parametrize("source_ranges, sorted_map_funcs, expected_result", [
    (   # seed to soil
        SortedRangeList([Range(55, 67), Range(79, 92)]),
        [MapFunc(Range(50, 97), 2), MapFunc(Range(98, 99), -48)],
        SortedRangeList([Range(57, 69), Range(81, 94)])
    ),
    (   # soil to fertilizer
        SortedRangeList([Range(57, 69), Range(81, 94)]),
        [MapFunc(Range(15, 51), -15), MapFunc(Range(52, 53), -15)],
        SortedRangeList([Range(57, 69), Range(81, 94)])
    ),
    (   # fertilizer to water
        SortedRangeList([Range(57, 69), Range(81, 94)]),
        [MapFunc(Range(0, 6), 42), MapFunc(Range(7, 10), 50), MapFunc(Range(11, 52), -11), MapFunc(Range(53, 60), -4)],
        SortedRangeList([Range(53, 56), Range(61, 69), Range(81, 94)]),
    ),
    (   # water to light
        SortedRangeList([Range(53, 56), Range(61, 69), Range(81, 94)]),
        [MapFunc(Range(18, 24), 70), MapFunc(Range(25, 94), -7)],
        SortedRangeList([Range(46, 49), Range(54, 62), Range(74, 87)]),
    ),
    (   # light to temperature
        SortedRangeList([Range(46, 49), Range(54, 62), Range(74, 87)]),
        [MapFunc(Range(45, 63), 36), MapFunc(Range(64, 76), 4), MapFunc(Range(77, 99), -32)],
        SortedRangeList([Range(45, 55), Range(78, 80), Range(82, 85), Range(90, 98)]),
    ),
    (   # temperature to humidity
        SortedRangeList([Range(45, 55), Range(78, 80), Range(82, 85), Range(90, 98)]),
        [MapFunc(Range(0, 68), 1), MapFunc(Range(69, 69), -69)],
        SortedRangeList([Range(46, 56), Range(78, 80), Range(82, 85), Range(90, 98)]),
    ),
    (   # humidity to location
        SortedRangeList([Range(46, 56), Range(78, 80), Range(82, 85), Range(90, 98)]),
        [MapFunc(Range(56, 92), 4), MapFunc(Range(93, 96), -37)],
        SortedRangeList([Range(46, 60), Range(82, 84), Range(86, 89), Range(94, 98)]),
        # SortedRangeList([Range(46, 55), Range(56, 59), Range(60, 60), Range(82, 84), Range(86, 89), Range(94, 96), Range(97, 98)])
    ),
])
def test_should_map_smaller_input_correctly(source_ranges, sorted_map_funcs, expected_result):
    # arrange
    range_mapper = RangeMapper(sorted_map_funcs)

    # act
    result = range_mapper.map(source_ranges)

    # assert
    assert result == expected_result

def test_map_func_map_should_work():
    # arrange
    map_func = MapFunc(Range(5, 10), delta=2)
    input_range = Range(5, 10)

    # act
    res = map_func.map(input_range)

    # assert
    assert res == Range(7, 12)
