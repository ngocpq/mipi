import abc
import json
from typing import List, Dict, Tuple
import numpy as np
from common import common, MethodPredictionResults


class PatchInfo:
    def __init__(self):
        self.patch_id = None
        self.bug_id = None
        self.snippets_info = None

    def parse_json(self, str_json):
        data = json.loads(str_json)
        self.from_json(data)

    def from_json(self, data):
        self.patch_id = data["PatchId"];
        self.bug_id = data["BugId"];
        self.snippets_info = []
        for trip in data["PatchedMethods"]:
            # triple = PatchTriple(code_context=trip["DevIntention"], org_code=trip["OrgCode"], pat_code=trip["PatCode"])
            triple = (trip["DevIntention"], trip["OrgCode"], trip["PatCode"])
            self.snippets_info.append(triple)

    def to_json(self):
        triples = []
        for dev_intent, org_code, pat_code in self.snippets_info:
            # triple = PatchTriple(code_context=trip["DevIntention"], org_code=trip["OrgCode"], pat_code=trip["PatCode"])
            trip = {'DevIntention': dev_intent, 'OrgCode': org_code, 'PatCode': pat_code}
            triples.append(trip)
        jo_patch = {'PatchId': self.patch_id,
                    'BugId': self.bug_id,
                    'PatchedMethods': triples}
        return json.dumps(jo_patch)


class SnippetEvaluationResult:
    sim_gain: float
    pat_distance: float
    predicted: int   # Incorrect: -1, Correct: 1, Unknown: 0

    def __init__(self, label, sim_gain, pat_distance):
        self.predicted = label
        self.sim_gain = sim_gain
        self.pat_distance = pat_distance

    def to_json(self):
        jo = {'SimGain': self.sim_gain,
              'PatDistance': self.pat_distance,
              'Predicted': self.predicted}
        return json.dumps(jo)


class PatchEvaluationResult:
    patch_id: str
    predicted: int   # Incorrect: -1, Correct: 1, Unknown: 0
    min_sim_gain: float
    max_pat_distance: float
    # snippets_results: Dict[Tuple[str, str, str], EvaluationResult]   # Tuple[dev, org, pat] -> score, class
    snippets_results: List[SnippetEvaluationResult]

    def __init__(self):
        self.patch_id = None
        self.predicted = None
        self.min_sim_gain = None
        self.max_pat_distance = None
        self.snippets_results = []

    def to_json(self):
        snippets_results = []
        for snip in self.snippets_results:
            snippets_results.append(snip.to_json())
        jo = {'PatchId': self.patch_id,
              'Predicted': self.predicted,
              'MinSimGain': self.min_sim_gain,
              'MaxPatDistance': self.max_pat_distance,
              'SnippetsResults': snippets_results}
        return json.dumps(jo)


class CodeMeaningPredictorBase(abc.ABC):

    def __init__(self, config):
        self.config = config

    @abc.abstractmethod
    def predict(self, code) -> MethodPredictionResults:
        ...


class MethodNameEmbeddingBase(abc.ABC):

    @abc.abstractmethod
    def get_vector(self, st) -> np.ndarray:
        ...

    def vectorize(self, sentences) -> List[np.ndarray]:
        vectors = []
        for st in sentences:
            method_vec = self.get_vector(st)
            vectors.append(method_vec)
        return vectors

    @abc.abstractmethod
    def similarity(self, s1, s2) -> float:
        ...

    @abc.abstractmethod
    def distance(self, s1, s2) -> float:
        ...


class MeaningSimilarityMeasurerBase(abc.ABC):

    def __init__(self, embedding_model: MethodNameEmbeddingBase):
        self.vectorizer = embedding_model

    @abc.abstractmethod
    def measure_distance(self, dev_name: str, predictions) -> float:
        ...


# class PatchEvaluatorBase(abc.ABC):
#     @abc.abstractmethod
#     def evaluate(self, dev_intention, org_prediction_result: MethodPredictionResults,
#                  pat_prediction_result: MethodPredictionResults) -> EvaluationResult:
#         ...
class PatchEvaluatorBase(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, dev_intention, org_prediction_result: MethodPredictionResults,
                 pat_prediction_result: MethodPredictionResults) -> SnippetEvaluationResult:
        ...

# class PatchEvaluatorBase(abc.ABC):
#     similarity_measurer: MeaningSimilarityMeasurerBase
#
#     def __init__(self, similarity_measurer: MeaningSimilarityMeasurerBase):
#         self.similarity_measurer = similarity_measurer
#
#     def evaluate(self, dev_intention, org_prediction_result: MethodPredictionResults,
#                  pat_prediction_result: MethodPredictionResults) -> EvaluationResult:
#
#         org_meanings = org_prediction_result.predictions
#         pat_meanings = pat_prediction_result.predictions
#
#         org_distance = self.similarity_measurer.measure_distance(dev_intention, org_meanings)
#         pat_distance = self.similarity_measurer.measure_distance(dev_intention, pat_meanings)
#         sim_gain = pat_distance - org_distance
#         if sim_gain < 0:
#             label = INCORRECT
#         else:
#             label = CORRECT
#         # result = {'Predicted': label, 'SimGain': sim_gain, 'PatDistance': pat_distance}
#         result = EvaluationResult(label=label, sim_gain=sim_gain, pat_distance=pat_distance)
#         return result
#
#
