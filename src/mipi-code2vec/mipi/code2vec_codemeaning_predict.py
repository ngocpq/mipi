from mipi.base_codemeaning_predictor import CodeMeaningPredictorBase
from common import common
from extractor import Extractor
from config import Config
from mipi.mipi_common import C2V_MODEL_PATH
from model_base import Code2VecModelBase

SHOW_TOP_CONTEXTS = 10
MAX_PATH_LENGTH = 8
MAX_PATH_WIDTH = 2
JAR_PATH = './JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar'


# def load_code_meaning_model(name: str = 'c2v', config=None) -> CodeMeaningPredictorBase:
#     if name == 'c2v':
#         if config is None:
#             config = Config(set_defaults=True, load_from_args=False, verify=False)
#             config.DL_FRAMEWORK = 'tensorflow'
#             config.PREDICT = True
#             config.MODEL_LOAD_PATH = C2V_MODEL_PATH
#         return Code2VecCodeMeaningPredictor(config)
#     else:
#         raise ValueError('Unsupported Code2Text model name [%s]' % name)


def load_model_dynamically(config: Config) -> Code2VecModelBase:
    assert config.DL_FRAMEWORK in {'tensorflow', 'keras'}
    if config.DL_FRAMEWORK == 'tensorflow':
        from tensorflow_model import Code2VecModel
    elif config.DL_FRAMEWORK == 'keras':
        from keras_model import Code2VecModel
    return Code2VecModel(config)


class Code2VecCodeMeaningPredictor(CodeMeaningPredictorBase):

    def __init__(self, config):
        model = load_model_dynamically(config)
        config.log('Done creating code2vec model')
        model.predict([])
        self.model = model
        self.config = config
        self.path_extractor = Extractor(config,
                                        jar_path=JAR_PATH,
                                        max_path_length=MAX_PATH_LENGTH,
                                        max_path_width=MAX_PATH_WIDTH)

    def predict(self, code):
        try:
            predict_lines, hash_to_string_dict, description_lines = self.path_extractor.extract_paths_code(code)
        except ValueError as e:
            print(e)
            raise e

        if len(predict_lines) > 1:
            print('WARNING: multiple methods in input code to "predict"')

        raw_prediction_results = self.model.predict(predict_lines)

        method_prediction_results = common.parse_prediction_results(
            raw_prediction_results, hash_to_string_dict,
            self.model.vocabs.target_vocab.special_words, topk=SHOW_TOP_CONTEXTS)
        if method_prediction_results is None or len(method_prediction_results) == 0:
            return None

        return method_prediction_results[0]

    def close_session(self):
        self.model.close_session()
