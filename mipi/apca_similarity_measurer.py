from typing import List

from common import MethodPredictionResults
from mipi.base_codemeaning_predictor import MeaningSimilarityMeasurerBase, MethodNameEmbeddingBase


# def load_meaning_distance_measurer(embedding: str = 'c2v', measurer: str = 'MinDist', config=None) -> MeaningSimilarityMeasurerBase:
#     txt_model = load_text_embedding(embedding)
#
#     if measurer == 'MinDist':
#         return MinDistanceMeaningSimilarityMeasurer(txt_model)
#     else:
#         raise ValueError('Unsupported measurer name [%s] ' % measurer)


class MinDistanceMeaningSimilarityMeasurer(MeaningSimilarityMeasurerBase):

    def __init__(self, embedding_model: MethodNameEmbeddingBase):
        super(MinDistanceMeaningSimilarityMeasurer, self).__init__(embedding_model)

    def measure_distance(self, dev_name: str, predictions) -> float:
        if predictions is None or len(predictions) == 0:
            return None
        predictions_distances = [(p['name'], p['probability'], self.vectorizer.distance(dev_name, p['name'])) for p in predictions]
        min_dist = None
        min_dist_prob = None
        min_dist_idx = None
        for idx, (name, prob, distance) in enumerate(predictions_distances):
            if distance is None:
                continue
            if min_dist is None or min_dist > distance:
                min_dist = distance
                min_dist_idx = idx
                min_dist_prob = prob
        if min_dist is None:
            return None
        score = min_dist
        return score
