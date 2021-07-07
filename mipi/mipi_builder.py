from mipi.apca_evaluators import SimGainEvaluator
from mipi.apca_similarity_measurer import load_meaning_distance_measurer
from mipi.apca_vectorizers import load_text_embedding
from mipi.base_codemeaning_predictor import MethodNameEmbeddingBase, CodeMeaningPredictorBase, \
    MeaningSimilarityMeasurerBase, PatchEvaluatorBase
from mipi.code2vec_codemeaning_predict import load_code_meaning_model
from mipi.mipi_app import Mipi


class MipiConfig:
    code_meaning_predictor: str
    text_embedding: str
    similarity_measurer: str
    correctness_evaluator: str

    def __init__(self, code_meaning_predictor='c2v', text_embedding='bert', similarity_measurer='MinDist',
                 correctness_evaluator='simgain'):
        self.code_meaning_predictor = code_meaning_predictor
        self.text_embedding = text_embedding
        self.similarity_measurer = similarity_measurer
        self.correctness_evaluator = correctness_evaluator


class MipiBuilder:
    code_meaning_predictors: dict[str, CodeMeaningPredictorBase]
    text_embedding_models: dict[str, MethodNameEmbeddingBase]
    # meaning_similarity_measurers: dict[str, MeaningSimilarityMeasurerBase]
    # correctness_evaluators: dict[str, PatchEvaluatorBase]

    def __init__(self):
        ...

    def build(self, config: MipiConfig = None):
        if config is None:
            config = MipiConfig()

        code_meaning_predictor = self.get_code_meaning_predictor(config.code_meaning_predictor)

        txt_embedding = self.get_text_embedding_model(config.text_embedding)

        similarity_measurer = load_meaning_distance_measurer(txt_embedding, config.similarity_measurer)

        patch_evaluator = self.build_evaluator(similarity_measurer, config.correctness_evaluator)
        return Mipi(code_meaning_predictor, patch_evaluator)

    def build_evaluator(self, similarity_measurer, evaluator_name):
        if evaluator_name == 'simgain':
            return SimGainEvaluator(similarity_measurer)

    def build_code_meaning_predictor(self, code_meaning_predictor_name):
        if code_meaning_predictor_name not in self.code_meaning_predictors:
            self.code_meaning_predictors[code_meaning_predictor_name] = load_code_meaning_model(
                code_meaning_predictor_name)
        return self.code_meaning_predictors[code_meaning_predictor_name]

    def get_text_embedding_model(self, text_embedding_name):
        if text_embedding_name not in self.text_embedding_models:
            self.text_embedding_models[text_embedding_name] = load_text_embedding(text_embedding_name)
        return self.text_embedding_models[text_embedding_name]
