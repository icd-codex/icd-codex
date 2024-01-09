"""Build a vector embedding from a networkX representation of the ICD hierarchy
using Transformers"""

from typing import Sequence, Union
from sentence_transformers import SentenceTransformer
import networkx as nx
import numpy as np
from tqdm import tqdm
from sklearn.neighbors import NearestNeighbors

def chunks(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))

class Icd2BERT:
    def __init__(self, lm="all-mpnet-base-v2"):
        """scikit-learn style transformer to learn embeddings from the ICD hierarchy
        
        Args:
            lm (str): Sentence transformer to use (https://www.sbert.net)
        """
        self.tokenizer = SentenceTransformer(lm)
        self.code2vec = {}
        self.nn = NearestNeighbors(n_neighbors=1)
        self.icd_codes = None
        self.icd_emebddings = None

    def fit(self, icd_hierarchy: nx.Graph, icd_codes: Sequence[str], **kwargs):
        """construct vector embedding of all ICD codes

        Args:
            icd_hierarchy (nx.Graph): Graph of ICD hierarchy
            icd_codes (Sequence[str]): ICD codes to embed
        """
        code2desc = []
        for code in icd_codes:
            desc = icd_hierarchy.nodes()[code]["description"]
            code2desc.append((code, desc))

        iter_ = list(chunks(code2desc, 512))
        for chunk in tqdm(iter_, unit="chunk"):
            codes, descs = zip(*chunk)
            embeds = self.tokenizer.encode(descs)
            for code, embed in zip(codes, embeds):
                self.code2vec[code] = embed

        self.icd_codes, self.icd_emebddings = zip(*self.code2vec.items())
        self.nn.fit(np.stack(self.icd_emebddings))
    
    def to_vec(self, icd_codes: Sequence[str]) -> np.ndarray:
        """Convert ICD codes to vectors

        Args:
            icd_codes (Sequence[str]): ICD codes to convert

        Returns:
            np.ndarray: Array of vectors
        """
        return np.stack([self.code2vec[code] for code in icd_codes])
    
    def to_code(self, vecs: Union[Sequence[Sequence], np.ndarray]) -> Sequence[str]:
        """decode continuous representation of ICD code(s) into the code itself

        Args:
            vecs (Union[Sequence[Sequence], np.ndarray]): continuous representation of ICD code(s)

        Returns:
            Sequence[str]: ICD code(s)
        """
        _, nbr_idxs = self.nn.kneighbors(vecs)
        return [self.icd_codes[i] for i in nbr_idxs.reshape(-1)]
