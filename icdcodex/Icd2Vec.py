"""Build a vector embedding from a networkX representation of the ICD hierarchy"""

from typing import Sequence, Union
import networkx as nx
import numpy as np
from node2vec import Node2Vec


class Icd2Vec:
    def __init__(
        self,
        num_embedding_dimensions: int,
        window: int,
        num_walks: int,
        walk_length: int = 10,
        **kwargs
    ):
        """scikit-learn style transformer to learn embeddings from the ICD hierarchy

        Arguments specified in the constructor are passed to node2vec.Node2vec gensim.models.Word2Vec, and the
        descriptions below are taken from their documentation

        Args:
            num_embedding_dimensions (int): number of dimensions in which to embed the ICD hierarchy
            window (int): Maximum distance between the current and predicted word within a sentence.
            num_walks: Number of walks per node. Defaults to 10.
            walk_length (int): Number of nodes in each walk. Defaults to 10.
            kwargs: arguments passed to the Node2Vec constructor
        """
        self.num_embedding_dimensions = num_embedding_dimensions
        self.window = window
        self.num_walks = num_walks
        self.walk_length = walk_length
        self.node2vec_kwargs = kwargs
        self.node2vec = None

    def fit(self, icd_hierarchy: nx.Graph, workers=1, **kwargs):
        """construct vector embedding of all ICD codes

        Args:
            icd_hierarchy (nx.Graph): Graph of ICD hierarchy
            workers (int, optional): Numbers of workers to perform walks. Defaults to 1.
            kwargs: arguments passed to the Node2Vec.fit
        """
        self.node2vec = Node2Vec(
            icd_hierarchy,
            dimensions=self.num_embedding_dimensions,
            workers=workers,
            quiet=True,
            **self.node2vec_kwargs
        ).fit(window=self.window, **kwargs)

    def transform(self, icd_codes: Sequence[str]) -> np.ndarray:
        """encode ICD code(s) into a matrix of continuously-valued representations of
        shape m x n where m = self.num_embedding_dimensions and n = len(icd_codes)

        Args:
            icd_codes (Sequence[str]): list of icd code(s)

        Raises:
            ValueError: If model is not fit beforehand

        Returns:
            np.ndarray: continuously-valued representations if ICD codes
        """
        if not self.node2vec:
            raise ValueError("model needs to be fit before")
        return np.stack(
            [self.node2vec.wv.get_vector(icd_code) for icd_code in icd_codes]
        )

    def vec2code(self, vecs: Union[Sequence[Sequence], np.ndarray]) -> Sequence[str]:
        """decode continuous representation of ICD code(s) into the code itself

        Args:
            vecs (Union[Sequence[Sequence], np.ndarray]): continuous representation of ICD code(s)

        Returns:
            Sequence[str]: ICD code(s)
        """
        vecs = np.array(vecs).reshape(-1, 1)
        return [self.node2vec.wv.most_similar(vec) for vec in vecs]
