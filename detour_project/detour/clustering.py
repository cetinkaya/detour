import numpy as np
from scipy.cluster.hierarchy import linkage, to_tree
from scipy.spatial.distance import pdist

from . import features

class HierarchicalClusterer:
    """This class implements Hierarchical Clustering for
    data points represented by their features."""

    def __init__(self, distance_calculation_method='ward'):
        self.distance_calculation_method = distance_calculation_method

    def cluster(self, features_list):
        """Given a list of feature lists, use hierarchical
        clustering to obtain a tree structure (dendogram) and
        return its root as well as the distance matrix showing
        pairwise distances between nodes in vector form."""
        data = np.vstack(features_list)
        dist = pdist(data)
        Z = linkage(dist, method='ward')
        return to_tree(Z), dist


class RoadClusterer(HierarchicalClusterer):
    """This class implements Hierarchical Clustering for Road
    objects based on their features."""

    def __init__(self, road_feature_extractor):
        """road_feature_extractor is a FeatureExtractor object
        that implements extract_features method."""
        super().__init__()
        self.road_feature_extractor = road_feature_extractor

    def cluster(self, roads):
        """Given a list of roads, and a feature_extractor use hierarchical
        clustering to obtain a tree structure (dendogram) and
        return its root as well as the distance matrix showing
        pairwise distances between nodes in vector form."""
        features_list = [self.road_feature_extractor.extract_features(road.xvalues, road.yvalues) for road in roads]
        return super().cluster(features_list)
