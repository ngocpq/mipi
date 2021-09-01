
C2V_MODEL_PATH = './models/java14_model/saved_model_iter8.release'
C2V_METHOD_NAME_EMBEDDING_MODEL_PATH = 'H:/MOPI_Github/scripts/models/Code2Vec_MethodNameEmbedding/java14_model/targets.txt'
SCOR_TERMS_EMBEDDING_MODEL_PATH = 'H:/MOPI_Github/scripts/models/SCOR_WordEmbeddings/embeddings/skipgram_vectors/N1500/model.output'

CORRECT = 'correct'
INCORRECT = 'incorrect'
UNKNOWN = 'unknown'


def method_name_2_sentence(method_name):
    if isinstance(method_name, str):
        if len(method_name.strip()) == 0:
            return ""
        arr = method_name.lower().split('|')
    elif isinstance(method_name, list):
        arr = method_name
    else:
        raise TypeError('Method name type is incorrect')

    sentence = arr[0].strip()
    for s in arr[1:]:
        sentence += " " + s.strip().lower()
    return sentence


def combine_ordered_metric(first_score, second_score):
    second_score_scaled = second_score/10
    temp = first_score
    while temp - int(temp) > 0:
        temp *= 10
        second_score_scaled /= 10
    score = first_score + second_score_scaled
    return score