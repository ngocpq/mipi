import logging
import scipy.spatial.distance as dist
import nltk
import numpy as np
import torch
from gensim.models import KeyedVectors as word2vec
import transformers as ppb

from mipi.base_codemeaning_predictor import MethodNameEmbeddingBase
from mipi.mipi_common import SCOR_TERMS_EMBEDDING_MODEL_PATH, C2V_METHOD_NAME_EMBEDDING_MODEL_PATH, method_name_2_sentence

logger = logging.getLogger()
success_logger = logging.getLogger("success")
error_logger = logging.getLogger("error")


class Code2VecMethodNameVectorizer(MethodNameEmbeddingBase):
    def __init__(self, w2v_model_file_path=C2V_METHOD_NAME_EMBEDDING_MODEL_PATH):
        self.model_path = w2v_model_file_path
        self.model_gensim = None

    def vectorize(self, method_names):
        if self.model_gensim is None:
            self.model_gensim = word2vec.load_word2vec_format(self.model_path, binary=False)

        vectors = []
        for method_name in method_names:
            method_vec = self.model_gensim.wv.get_vector(method_name)
            vectors.append(method_vec)
        return vectors

    def get_model(self):
        if self.model_gensim is None:
            self.model_gensim = word2vec.load_word2vec_format(self.model_path, binary=False)
        return self.model_gensim

    def get_vector(self, method_name):
        if method_name in self.model_gensim.wv.vocab:
            return self.model_gensim.wv.get_vector(method_name)
        else:
            ps = nltk.stem.PorterStemmer()
            query_word = ps.stem(method_name)
            try:
                return self.model_gensim.wv.get_vector(query_word)
            except KeyError as keyError:
                logger.error('methodName: "%s" out of vocabulary of code2vec\terrorMsg: %s' % (method_name, keyError))
                return None

    def distance(self, sentence_1, sentence_2):
        model = self.get_model()
        if sentence_1 is None or sentence_2 is None:
            return None
        return model.wmdistance(sentence_1, sentence_2)

    def similarity(self, sentence_1, sentence_2):
        model = self.get_model()
        if sentence_1 is None or sentence_2 is None:
            return None
        w1 = self.find_name_in_vocabulary(sentence_1)
        w2 = self.find_name_in_vocabulary(sentence_2)
        if w1 is None or w2 is None:
            return None
        return model.similarity(w1, w2)

    def find_name_in_vocabulary(self, name):
        word_variants = self.get_word_variants(name)
        words = []
        if name == "binsearch":
            words = self.get_word_variants("bin|search")
        if name == "powerset":
            words = self.get_word_variants("power|set")
        if name == "quicksort":
            words = self.get_word_variants("quick|sort")
        if name == "mergesort":
            words = self.get_word_variants("merge|sort")

        word_variants = words + word_variants

        for word in word_variants:
            if word in self.model_gensim:
                return word
        return None

    def get_word_variants(self, word):
        result = []
        result.append(word)

        if word.endswith("s"):
            w = word[:- 1]
            result.append(w)

        if word.endswith("es"):
            w = word[:-2]
            result.append(w)
        return result


class SCORMethodNameVectorizer(MethodNameEmbeddingBase):
    def __init__(self, w2v_model_file_path=SCOR_TERMS_EMBEDDING_MODEL_PATH):
        self.model_path = w2v_model_file_path
        self.model_gensim = None

    def get_model(self):
        if self.model_gensim is None:
            self.model_gensim = word2vec.load(self.model_path)
        return self.model_gensim

    def vectorize(self, method_names):
        self.get_model()
        vectors = []
        for method_name in method_names:
            method_vec = self.get_vector(method_name)
            vectors.append(method_vec)

        return vectors

    def get_vector(self, name):
        self.get_model()
        words = name.split('|')
        sum_vec = None
        for w in words:
            try:
                ps = nltk.stem.PorterStemmer()
                query_word = ps.stem(w)
                v = self.model_gensim.wv.get_vector(query_word)
                if sum_vec is None:
                    sum_vec = np.asarray(v)
                else:
                    sum_vec = sum_vec + np.asarray(v)
            except KeyError as keyError:
                logger.error('methodName: "%s". Out of vocabulary word "%s"\terrorMsg: %s' % (name, w, keyError))
        return sum_vec

    def distance(self, method_name1, method_name2):
        self.get_model()
        if method_name1 is None or method_name1 is None:
            return None
        sentence_1 = method_name1.replace('|', ' ')
        sentence_2 = method_name2.replace('|', ' ')
        score = self.model_gensim.wv.wmdistance(sentence_1, sentence_2)
        return score

    def similarity(self, method_name1, method_name2):
        model = self.get_model()
        if method_name1 is None or method_name1 is None:
            return None
        v1 = None
        for w in method_name1.split('|'):
            if w not in model.wv.vocab:
                continue
            if v1 is None:
                v1 = np.asarray(model.wv.get_vector(w))
            else:
                v1 = np.asarray(v1) + np.asarray(model.wv.get_vector(w))

        v2 = None
        for w in method_name2.split('|'):
            if w not in model.wv.vocab:
                continue
            if v2 is None:
                v2 = np.asarray(model.wv.get_vector(w))
            else:
                v2 = np.asarray(v2) + np.asarray(model.wv.get_vector(w))
        if v1 is None or v2 is None:
            return None
        score = 1 - dist.cosine(v1, v2)
        return score


class BertMethodNameVectorizer(MethodNameEmbeddingBase):
    def __init__(self, pretrained_weights='distilbert-base-uncased'):
        self.model_class, self.tokenizer_class, self.pretrained_weights = (ppb.DistilBertModel,
                                                                           ppb.DistilBertTokenizer,
                                                                           pretrained_weights)
        self.tokenizer = self.tokenizer_class.from_pretrained(pretrained_weights)
        self.model = self.model_class.from_pretrained(pretrained_weights)
        # self.max_len = 10

    def get_vector(self, name):
        names = [name]
        return self.vectorize(names)

    def vectorize(self, method_names):
        tokenized = list(map(lambda x: self.tokenizer.encode(x, add_special_tokens=True), method_names))
        max_len = max([len(i) for i in tokenized])
        padded = np.array([i + [0] * (max_len - len(i)) for i in tokenized])
        input_ids = torch.tensor(np.array(padded)).type(torch.LongTensor)
        # attention_mask = torch.tensor(np.where(padded != 0, 1, 0)).type(torch.LongTensor)

        with torch.no_grad():
            last_hidden_states = self.model(input_ids)

        vectors = last_hidden_states[0][:, 0, :].numpy()
        return vectors

    def normalize(self, method_name):
        return method_name_2_sentence(method_name)

    def distance(self, sentence_1, sentence_2):
        if sentence_1 is None or sentence_2 is None:
            return None
        sentence_1 = self.normalize(sentence_1)
        sentence_2 = self.normalize(sentence_2)

        if sentence_1 == sentence_2:
            return 0.0

        names = [sentence_1, sentence_2]
        vectors = self.vectorize(names)
        return dist.cosine(vectors[0], vectors[1])

    def similarity(self, sentence_1, sentence_2):
        if sentence_1 is None or sentence_2 is None:
            return None
        sentence_1 = self.normalize(sentence_1)
        sentence_2 = self.normalize(sentence_2)
        names = [sentence_1, sentence_2]
        vectors = self.vectorize(names)
        return 1 - dist.cosine(vectors[0], vectors[1])


if __name__ == "__main__":
    print('Test SCOR')
    scor_vectorizer = SCORMethodNameVectorizer()
    bert_vectorizer = BertMethodNameVectorizer()

    print('Test Code2Vec')
    c2v_vectorizer = Code2VecMethodNameVectorizer()
    model = c2v_vectorizer.get_model()

    test_wmd_similarity = True
    if test_wmd_similarity:
        num_best = 10
        # instance = WmdSimilarity(model, num_best=10)
        while True:
            query = input("query method name: [Enter to exit]? ")
            if 0 == len(query.strip()):
                exit()
            # sims = instance[query]
            try:
                sims = model.similar_by_word(query, num_best)
                print('Query:')
                print(query)
                for i in range(num_best):
                    print
                    print('sim = %.4f\t%s' % (sims[i][1], sims[i][0]))
            except Exception as ex:
                print("Error %s" % ex)
        exit(0)

    while True:
        sentence1 = input("sentence 1: [Enter to exit]? ")
        if 0 == len(sentence1.strip()):
            exit()

        sentence2 = input("sentence 2: [Enter to exit]? ")
        if 0 == len(sentence2.strip()):
            exit()

        print("Word Mover's Distance between '%s' and '%s'" % (sentence1, sentence2))
        try:
            wm_dist = model.wmdistance(sentence1, sentence2)
            print('wmdistance: %s' % wm_dist)
        except Exception as ex:
            print("wmdistance Error: %s" % ex)
        try:
            cosine_dist = model.distance(sentence1, sentence2)
            print('cosine_dist: %s' % cosine_dist)
        except Exception as ex:
            print("cosine_dist Error: %s" % ex)

        print("Distance between '%s' and '%s'" % (sentence1, sentence2))
        try:
            wm_dist = c2v_vectorizer.distance(sentence1, sentence2)
            print('c2v_vectorizer.distance: %s' % wm_dist)
        except Exception as ex:
            print("c2v_vectorizer Error: %s" % ex)
        try:
            wm_dist = scor_vectorizer.distance(sentence1, sentence2)
            print('scor_vectorizer.distance: %s' % wm_dist)
        except Exception as ex:
            print("scor_vectorizer Error: %s" % ex)
        try:
            wm_dist = bert_vectorizer.distance(sentence1, sentence2)
            print('bert_vectorizer.distance: %s' % wm_dist)
        except Exception as ex:
            print("bert_vectorizer Error: %s" % ex)

        print("Similarity between '%s' and '%s'" % (sentence1, sentence2))
        try:
            wm_dist = c2v_vectorizer.similarity(sentence1, sentence2)
            print('c2v_vectorizer.similarity: %s' % wm_dist)
        except Exception as ex:
            print("c2v_vectorizer Error: %s" % ex)
        try:
            wm_dist = scor_vectorizer.similarity(sentence1, sentence2)
            print('scor_vectorizer.similarity: %s' % wm_dist)
        except Exception as ex:
            print("scor_vectorizer Error: %s" % ex)
        try:
            wm_dist = bert_vectorizer.similarity(sentence1, sentence2)
            print('bert_vectorizer.similarity: %s' % wm_dist)
        except Exception as ex:
            print("bert_vectorizer Error: %s" % ex)
