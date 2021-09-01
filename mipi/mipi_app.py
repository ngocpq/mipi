import json

from mipi.apca_evaluators import SimGainEvaluator
from mipi.apca_similarity_measurer import MinDistanceMeaningSimilarityMeasurer
from mipi.apca_vectorizers import Code2VecMethodNameVectorizer, BertMethodNameVectorizer, \
    SCORMethodNameVectorizer
from mipi.base_codemeaning_predictor import PatchInfo, CodeMeaningPredictorBase, PatchEvaluatorBase, \
    PatchEvaluationResult, MeaningSimilarityMeasurerBase

from mipi.code2vec_codemeaning_predict import Code2VecCodeMeaningPredictor
from config import Config
from mipi.mipi_common import C2V_MODEL_PATH, INCORRECT


def load_text_embedding(name: str = 'c2v', config=None):
    if name == 'c2v':
        return Code2VecMethodNameVectorizer()
    elif name == 'bert':
        return BertMethodNameVectorizer()
    elif name == 'scor':
        return SCORMethodNameVectorizer()
    else:
        raise ValueError('unsupported embedding [%s]' % name)


def load_code_meaning_model(name: str = 'c2v', config=None) -> CodeMeaningPredictorBase:
    if name == 'c2v':
        if config is None:
            config = Config(set_defaults=True, load_from_args=False, verify=False)
            config.DL_FRAMEWORK = 'tensorflow'
            config.PREDICT = True
            config.MODEL_LOAD_PATH = C2V_MODEL_PATH
        return Code2VecCodeMeaningPredictor(config)
    else:
        raise ValueError('Unsupported Code2Text model name [%s]' % name)


def load_meaning_distance_measurer(embedding: str = 'bert', measurer: str = 'MinDist', config=None) -> MeaningSimilarityMeasurerBase:
    txt_model = load_text_embedding(embedding)

    if measurer == 'MinDist':
        return MinDistanceMeaningSimilarityMeasurer(txt_model)
    else:
        raise ValueError('Unsupported measurer name [%s] ' % measurer)


def getPatchCorrectnessEvaluator(evaluator_name, measurer: MeaningSimilarityMeasurerBase) -> PatchEvaluatorBase:
    if evaluator_name == 'SimGain':
        return SimGainEvaluator(measurer)
    return None


class Mipi:
    code_meaning_model: CodeMeaningPredictorBase
    snippet_evaluator: PatchEvaluatorBase

    def __init__(self, code2text_name='c2v', txt_embedding_name='bert', measurer_name='MinDist', evaluator_name: str = 'SimGain'):
        self.code_meaning_model = load_code_meaning_model(code2text_name)
        measurer = load_meaning_distance_measurer(txt_embedding_name, measurer_name)
        # self.patch_evaluator = PatchEvaluatorBase(measurer)
        self.snippet_evaluator = getPatchCorrectnessEvaluator(evaluator_name, measurer)

    def evaluate(self, patch: PatchInfo) -> PatchEvaluationResult:
        result = PatchEvaluationResult()
        result.patch_id = patch.patch_id
        for dev_intention, org_code, pat_code in patch.snippets_info:
            org_prediction_result = self.code_meaning_model.predict(org_code)
            pat_prediction_result = self.code_meaning_model.predict(pat_code)

            snippet_result = self.snippet_evaluator.evaluate(dev_intention, org_prediction_result, pat_prediction_result)
            result.snippets_results.append(snippet_result)

        for snp_result in result.snippets_results:
            if result.predicted is None or snp_result.predicted == INCORRECT:
                result.predicted = snp_result.predicted

            if result.min_sim_gain is None or (result.min_sim_gain > snp_result.sim_gain):
                result.min_sim_gain = snp_result.sim_gain

            if result.max_pat_distance is None or (result.max_pat_distance < snp_result.pat_distance):
                result.max_pat_distance = snp_result.pat_distance

        return result


def load_patches_from_file(patches_json_file):
    with open(patches_json_file, "r", encoding="utf8") as file:
        patches_json = json.load(file)
    patches = []
    for jo_patch in patches_json:
        patch = PatchInfo()
        patch.from_json(jo_patch)
        patches.append(patch)
    return patches


if __name__ == '__main__':
    dataset_json_file = 'SamplePatches.json'
    patches = load_patches_from_file(dataset_json_file)

    obj_mipi = Mipi()

    for p in patches:
        rs = obj_mipi.evaluate(p)
        print('Results: \n%s' % rs)
        print('Json resuls: \n%s' % rs.to_json())

    # exit(0)
    #
    # c2v_config = Config(set_defaults=True, load_from_args=True, verify=True)
    #
    # predictor = Code2VecCodeMeaningPredictor(c2v_config)
    # while True:
    #     print('Modify the file: "input.java" and press any key when ready, or "q" / "quit" / "exit" to exit')
    #     user_input = input()
    #     if user_input.lower() in ['exit', 'quit', 'q']:
    #         print('Exiting...')
    #         break
    #
    #     input_file = "Input.java"
    #     code = read_file(input_file)
    #     # code = 'public void getMethod(int a){ return this.x +a;}'
    #     method_prediction = predictor.predict(code)
    #
    #     # for method_prediction in method_prediction_results:
    #     print('Original name:\t' + method_prediction.original_name)
    #     for name_prob_pair in method_prediction.predictions:
    #         print('\t(%f) predicted: %s' % (name_prob_pair['probability'], name_prob_pair['name']))
    #     print('Attention:')
    #     for attention_obj in method_prediction.attention_paths:
    #         print('%f\tcontext: %s,%s,%s' % (
    #         attention_obj['score'], attention_obj['token1'], attention_obj['path'], attention_obj['token2']))
    #     if c2v_config.EXPORT_CODE_VECTORS:
    #         print('Code vector:')
    #         print(' '.join(map(str, method_prediction.code_vector)))
    #
    # predictor.close_session()
