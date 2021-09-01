import abc

from common import MethodPredictionResults
from mipi.base_codemeaning_predictor import SnippetEvaluationResult, PatchEvaluatorBase, MeaningSimilarityMeasurerBase
from mipi.mipi_common import INCORRECT, CORRECT


class SimGainEvaluator(PatchEvaluatorBase):
    similarity_measurer: MeaningSimilarityMeasurerBase

    def __init__(self, similarity_measurer: MeaningSimilarityMeasurerBase):
        self.similarity_measurer = similarity_measurer

    def evaluate(self, dev_intention, org_prediction_result: MethodPredictionResults,
                 pat_prediction_result: MethodPredictionResults) -> SnippetEvaluationResult:

        org_meanings = org_prediction_result.predictions
        pat_meanings = pat_prediction_result.predictions

        org_distance = self.similarity_measurer.measure_distance(dev_intention, org_meanings)
        pat_distance = self.similarity_measurer.measure_distance(dev_intention, pat_meanings)
        sim_gain = org_distance - pat_distance
        if sim_gain < 0:
            label = INCORRECT
        else:
            label = CORRECT
        # result = {'Predicted': label, 'SimGain': sim_gain, 'PatDistance': pat_distance}
        result = SnippetEvaluationResult(label=label, sim_gain=sim_gain, pat_distance=pat_distance)
        return result


