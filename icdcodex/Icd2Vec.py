"""Build a vector embedding from a networkX representation of the ICD hierarchy"""

from typing import Sequence
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
        """[summary]

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
        """[summary]

        Args:
            icd_codes (Sequence[str]): [description]

        Raises:
            ValueError: [description]

        Returns:
            np.ndarray: [description]
        """
        if not self.node2vec:
            raise ValueError

    def vec2code(self, vecs) -> Sequence[str]:
        """[summary]

        Args:
            vecs ([type]): [description]

        Returns:
            Sequence[str]: [description]
        """
        raise NotImplementedError
