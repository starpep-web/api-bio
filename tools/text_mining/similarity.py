import os
import tempfile
import fasttext
import numpy as np
from dataclasses import dataclass
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tools.utils import get_model_path


@dataclass
class SimilarPeptides:
    sequence: str
    vector: list
    similarity: float


@dataclass
class PeptideSimilarityResult:
    query: str
    vector: list
    results: List[SimilarPeptides]


class TfidfSimilarity:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(lowercase=False, analyzer='char')
        self.peptide_vectors = np.matrix(0)
        self.peptides = np.array(0)

    def train(self, peptides: np.array):
        self.peptides = peptides
        self.peptide_vectors = self.vectorizer.fit_transform(peptides).todense()

    def transform(self, peptide: str) -> np.matrix:
        return self.vectorizer.transform([peptide]).todense()

    def compute_cosine_similarities(self, query: np.matrix) -> np.array:
        return cosine_similarity(np.asarray(self.peptide_vectors), np.asarray(query))

    def compare_query(self, query: str, **kwargs) -> PeptideSimilarityResult:
        limit = kwargs.get('limit') or len(self.peptide_vectors)
        threshold = kwargs.get('treshold') or -1

        query_matrix = self.transform(query)
        similarities = self.compute_cosine_similarities(query_matrix).flatten()  # Works for single query

        sorted_similarity_permutation = np.argsort(similarities)[::-1]
        sorted_vectors = self.peptide_vectors[sorted_similarity_permutation]
        sorted_peptides = self.peptides[sorted_similarity_permutation]

        sorted_results = []

        for index in range(limit):
            sequence = sorted_peptides[index]
            vector = np.asarray(sorted_vectors[index])
            similarity = similarities[sorted_similarity_permutation[index]]

            if similarity < threshold:
                break

            sorted_results.append(SimilarPeptides(sequence, list(vector.flatten()), similarity))

        query_vector = list(np.asarray(query_matrix).flatten())
        return PeptideSimilarityResult(query, query_vector, sorted_results)


class FastTextSimilarity:
    MODEL_NAME = 'text_mining/similarity/pep-fasttext.bin'

    def __init__(self):
        self.model = fasttext.FastText._FastText()  # Only for typing reasons.

    def train(self, peptides: np.array, **kwargs):
        epochs = kwargs.get('epochs') or 25

        peptides_as_text = ' '.join(list(map(str, peptides.tolist())))
        tmp_file, tmp_path = tempfile.mkstemp()
        try:
            with os.fdopen(tmp_file, 'w') as file:
                file.write(peptides_as_text)

            self.model = fasttext.train_unsupervised(tmp_path, model='skipgram', minCount=1, wordNgrams=1, epoch=epochs)
        finally:
            os.remove(tmp_path)

        model_path = get_model_path(FastTextSimilarity.MODEL_NAME)
        self.model.save_model(model_path)

    def load(self):
        fasttext.FastText.eprint = lambda x: None
        model_path = get_model_path(FastTextSimilarity.MODEL_NAME)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f'Model path for {self.__class__.__name__} does not exist.')

        self.model = fasttext.load_model(model_path)

    def compare_query(self, query: str, **kwargs) -> PeptideSimilarityResult:
        limit = kwargs.get('limit') or 10
        threshold = kwargs.get('treshold') or -1

        neighbors = self.model.get_nearest_neighbors(query, k=limit)
        results = []

        for similarity, sequence in neighbors:
            if similarity < threshold:
                break

            vector = list(map(float, self.model.get_word_vector(sequence)))
            results.append(SimilarPeptides(sequence, vector, similarity))

        query_vector = list(map(float, self.model.get_word_vector(query)))
        return PeptideSimilarityResult(query, query_vector, results)
