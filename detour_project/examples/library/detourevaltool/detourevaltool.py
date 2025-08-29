# This file is provided in relation to the test selection competition pipeline
# provided at https://github.com/christianbirchler-org/sdc-testing-competition
# It request competition_pb2_grpc and competition_pb2 modules that can be
# obtained from the sample tool in the same repository.

import os
import competition_pb2_grpc
import competition_pb2
import grpc
import concurrent.futures as fut
from detour.detour import DETOUR
from detour.road import Road
from detour.features import CurvatureBasedRoadFeatureExtractor
from detour.clustering import RoadClusterer


class DETOUREvalTool(competition_pb2_grpc.CompetitionToolServicer):
    """
    DETOUREvalTool is a test selector for SDC Testing Competition.
    """

    def Name(self, request, context):
        """Provide the name of the tool."""
        return competition_pb2.NameReply(name="detour")

    def Initialize(self, request_iterator, context):
        """Initialize the tool with oracels."""
        self.executed_roads = []
        self.not_executed_roads = []
        for oracle in request_iterator:
            oracle: competition_pb2.Oracle = oracle
            xvalues = [road_point.x for road_point in oracle.testCase.roadPoints]
            yvalues = [road_point.y for road_point in oracle.testCase.roadPoints]
            self.executed_roads.append(Road(oracle, xvalues, yvalues, oracle.hasFailed, False))

        return competition_pb2.InitializationReply(ok=True)

    def Select(self, request_iterator, context):
        """Test case selection based on given request iterator."""
        for sdc_test_case in request_iterator:
            sdc_test_case: competition_pb2.SDCTestCase = sdc_test_case
            xvalues = [road_point.x for road_point in sdc_test_case.roadPoints]
            yvalues = [road_point.y for road_point in sdc_test_case.roadPoints]
            self.not_executed_roads.append(Road(sdc_test_case, xvalues, yvalues, None, True))

        feature_extractor = features.CurvatureBasedRoadFeatureExtractor(args.road_section_count)
        road_clusterer = clustering.RoadClusterer(feature_extractor)
        detour_ob = DETOUR(self.executed_roads, self.not_executed_roads, road_clusterer)

        selected_nodes = detour_ob.select(min_select_ratio=0.05,
                                          max_select_ratio=0.4,
                                          m_closest_neighbor_count=4,
                                          w_selection_threshold=4)
        for i in range(len(selected_nodes)):
            sdc_test_case = selected_nodes[i].id
            yield competition_pb2.SelectionReply(testId=sdc_test_case.testId)


if __name__ == "__main__":
    print("Start test selector")
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port")
    args = parser.parse_args()
    GRPC_PORT = args.port
    GRPC_URL = "[::]:" + GRPC_PORT

    server = grpc.server(fut.ThreadPoolExecutor(max_workers=2))
    competition_pb2_grpc.add_CompetitionToolServicer_to_server(DETOUR(), server)

    server.add_insecure_port(GRPC_URL)
    print("Start server on port {}".format(GRPC_PORT))
    server.start()
    print("Server is running")
    server.wait_for_termination()
    print("Server terminated")
