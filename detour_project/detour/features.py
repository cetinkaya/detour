import numpy as np

from abc import abstractmethod
from . import roadgeometry

class RoadFeatureExtractor:
    def __init__(self):
        pass

    @abstractmethod
    def extract_features(self, xvalues, yvalues):
        """When (x, y) Cartesian coordinates of a road
        is given this method extracts features and returns
        them as a list of numeric values."""


class CurvatureBasedRoadFeatureExtractor(RoadFeatureExtractor):
    def __init__(self, road_section_count):
        super().__init__()
        self.road_section_count = road_section_count

    @staticmethod
    def reduce(kappas, arclengths, N):
        """Reduces given lists of kappas and arclengths to shorter
        versions by approximating an underlying road with a road
        with N number of sections.

        The approximation algorithm works iteratively on the road
        described curvature and arc length values (kappas, arclengths)
        of road sections. At each iteration two road sections are
        selected and merged. The new road section has the curvature value
        set as the average curvature of the merged sections and its arclength
        is the sum of the merged sections. The selection is done so that after
        the merging the curvature of the new road (merging changes the road) is
        closest to the road beforehand in comparison to other merging options."""

        kappas_list = [float(kappas[i]) for i in range(kappas.shape[0])]
        arclengths_list = [float(arclengths[i]) for i in range(kappas.shape[0])]
        all_kappas_list = [[k] for k in kappas_list]
        all_arclengths_list = [[a] for a in arclengths_list]

        # Iterate until there are N road sections
        while len(kappas_list) > N:
            cur_len = len(kappas_list)
            kappa_avgs = []
            arclength_sums = []
            errors = []

            # Calculate curvature errors for all possible merging options
            for j in range(cur_len - 1):
                arclength_sum = arclengths_list[j] + arclengths_list[j + 1]
                kappa_avg = (kappas_list[j] * arclengths_list[j] + kappas_list[j + 1] * arclengths_list[
                    j + 1]) / arclength_sum
                error = sum(
                    [np.abs(kappa_avg - k) * a for (k, a) in zip(all_kappas_list[j], all_arclengths_list[j])]) + sum(
                    [np.abs(kappa_avg - k) * a for (k, a) in zip(all_kappas_list[j + 1], all_arclengths_list[j + 1])])
                kappa_avgs.append(kappa_avg)
                arclength_sums.append(arclength_sum)
                errors.append(error)

            # Choose merging index that minimizes the error
            merge_index = int(np.argmin(errors))

            # Complete merging
            new_kappas_list = []
            new_arclengths_list = []
            new_all_kappas_list = []
            new_all_arclengths_list = []
            for j in range(merge_index):
                new_kappas_list.append(kappas_list[j])
                new_arclengths_list.append(arclengths_list[j])
                new_all_kappas_list.append(all_kappas_list[j])
                new_all_arclengths_list.append(all_arclengths_list[j])

            new_kappas_list.append(kappa_avgs[merge_index])
            new_arclengths_list.append(arclength_sums[merge_index])
            new_all_kappas_list.append(all_kappas_list[merge_index] + all_kappas_list[merge_index + 1])
            new_all_arclengths_list.append(all_arclengths_list[merge_index] + all_arclengths_list[merge_index + 1])

            for j in range(merge_index + 2, len(kappas_list)):
                new_kappas_list.append(kappas_list[j])
                new_arclengths_list.append(arclengths_list[j])
                new_all_kappas_list.append(all_kappas_list[j])
                new_all_arclengths_list.append(all_arclengths_list[j])

            kappas_list = new_kappas_list
            arclengths_list = new_arclengths_list
            all_kappas_list = new_all_kappas_list
            all_arclengths_list = new_all_arclengths_list

        # return curvature and arc length values of the road has N road sections
        return kappas_list, arclengths_list

    def extract_features(self, xvalues, yvalues):
        """Extract features as a concatenated list of initial orientation,
        together with curvature and arc length values """
        t0, k, a = roadgeometry.xy2ka(np.array(xvalues), np.array(yvalues))
        klist, alist = CurvatureBasedRoadFeatureExtractor.reduce(k, a, self.road_section_count)
        return [t0] + klist + alist

