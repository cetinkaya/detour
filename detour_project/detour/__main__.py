from . import clustering
from . import detour
from . import features
from . import road

import argparse
import json

def setup_parser():
    """Setup function for DETOUR's command line interface argument parser."""
    parser =argparse.ArgumentParser(description="DETOUR cli tool")

    # JSON Files for executed not-executed and output tests
    parser.add_argument("--executed-filepath", type=str, default="executed.json",
                        help="Filepath for the json file that provides executed test cases.")
    parser.add_argument("--not-executed-filepath", type=str, default="not-executed.json",
                        help="Filepath for the json file that provides not-executed (prioritizable/selectable) test cases.")
    parser.add_argument("--output-filepath", type=str, default="output.json",
                        help="Filepath for the json file that DETOUR outputs after prioritization/selection.")

    # Functionality: Test Case Prioritization, Test Case Selection
    parser.add_argument("--functionality", choices=["prioritization", "selection"], default="prioritization",
                        help="Functionality to apply on not-executed tests, whether to prioritize them or to select among them.")

    # Test Case Prioritization-related arguments
    parser.add_argument("--prioritization-ratio", type=float, default=1.0,
                        help="Ratio of tests to be returned among not-executed tests after prioritization.")

    # Test Case Selection-related arguments
    parser.add_argument("--selection-min-ratio", type=float, default=0.05,
                        help="Minimum ratio of tests to be returned among not-executed tests after selection.")
    parser.add_argument("--selection-max-ratio", type=float, default=0.4,
                        help="Maximum ratio of tests to be returned among not-executed tests after selection.")
    parser.add_argument("--selection-m-closest-neighbor-count", type=int, default=4,
                        help="Number of closest neighboring test cases deemed to be passing in the stopping criteria for selection.")
    parser.add_argument("--selection-w-selection-threshold", type=int, default=4,
                        help="Threshold for number of last selected test cases that are allowed to have m-closest-neighbor-count of neighbors passing to identify the stopping criteria for selection.")


    # Road section count for feature extraction
    parser.add_argument("--road_section-count", type=int, default=6,
                        help="Road section count for extracting curvature/arclength features from road test cases.")

    # Random seed
    parser.add_argument("--random-seed", type=int, default=0,
                        help="Seed for random operations in DETOUR algorithm.")

    return parser

def get_roads_from_json_filepath(json_filepath, is_executed):
    """This function creates a list of Road objects
    from roads specified in a json file. The json file has the template
    [road1_spec, road2_spec, ...] where road1_spec has the template
    {"meta_data": {"test_info": {"test_outcome": "FAIL"}}
     "road_points" [{"x": float, "y": float}, ...]} for Failing executed-tests
    {"meta_data": {"test_info": {"test_outcome": "PASS"}}
     "road_points" [{"x": float, "y": float}, ...]} for Passing executed-tests
    {"road_points" [{"x": float, "y": float}, ...]} for not-executed-tests
    It is allowable to have other keys such as ids and information about
    test-execution configurations as long as the keys above are provided.
    The parameter is_executed (True/False) specifies whether the provided
    json file contains roads that are executed or not-executed. Executed
    roads (tests) should have the test_outcome.
     """
    roads = []
    with open(json_filepath, 'r') as file:
        data = json.load(file)
        for entry in data:
            xvalues = [point["x"] for point in entry["road_points"]]
            yvalues = [point["y"] for point in entry["road_points"]]
            if is_executed:
                is_failing = entry["meta_data"]["test_info"]["test_outcome"] == "FAIL"
                is_selectable = False
                road_to_add = road.Road(entry,
                                        xvalues,
                                        yvalues,
                                        is_failing,
                                        is_selectable)
            else:
                is_failing = None
                is_selectable = True
                road_to_add = road.Road(entry,
                                        xvalues,
                                        yvalues,
                                        is_failing,
                                        is_selectable)
            roads.append(road_to_add)

    return roads

def main():
    """Main entry point for DETOUR command line tool."""
    parser = setup_parser()
    args = parser.parse_args()

    executed_roads = get_roads_from_json_filepath(args.executed_filepath, True)
    not_executed_roads = get_roads_from_json_filepath(args.not_executed_filepath, False)

    feature_extractor = features.CurvatureBasedRoadFeatureExtractor(args.road_section_count)
    road_clusterer = clustering.RoadClusterer(feature_extractor)

    detour_ob = detour.DETOUR(executed_roads, not_executed_roads, road_clusterer, args.random_seed)

    if args.functionality == 'prioritization':
        output_roads = detour_ob.prioritize(args.prioritization_ratio)
    else:
        output_roads = detour_ob.select(args.selection_min_ratio,
                                        args.selection_max_ratio,
                                        args.selection_m_closest_neighbor_count,
                                        args.selection_w_selection_threshold)

    output_data = [road_ob.id for road_ob in output_roads]
    with open(args.output_filepath, 'w') as file:
        json.dump(output_data, file, indent=4)


main()
