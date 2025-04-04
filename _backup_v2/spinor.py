# spinor.py

import numpy as np
from typing import Union, List, Optional

class Spinor:
    def __init__(self, vector: Union[list, np.ndarray]):
        self.vector = np.array(vector, dtype=np.float32)

    def rotate(self, other: 'Spinor') -> 'Spinor':
        return Spinor(np.add(self.vector, other.vector))

    def bind(self, other: 'Spinor') -> 'Spinor':
        return Spinor(np.multiply(self.vector, other.vector))

    def similarity(self, other: 'Spinor') -> float:
        norm_self = np.linalg.norm(self.vector)
        norm_other = np.linalg.norm(other.vector)
        if norm_self == 0 or norm_other == 0:
            return 0.0
        return float(np.dot(self.vector, other.vector) / (norm_self * norm_other))

    def permute(self) -> 'Spinor':
        return Spinor(np.roll(self.vector, 1))

    def __repr__(self):
        return f"Spinor({self.vector[:5]}...)"

    @classmethod
    def from_label(cls, label: str) -> 'Spinor':
        np.random.seed(abs(hash(label)) % (2**32))
        return cls(np.random.normal(0, 1, 512))

    @classmethod
    def from_embedding(cls, vec: np.ndarray) -> 'Spinor':
        return cls(np.array(vec))

    @classmethod
    def bind_all(cls, spinors: List['Spinor']) -> 'Spinor':
        result = spinors[0]
        for s in spinors[1:]:
            result = result.bind(s)
        return result

    @classmethod
    def encode_init(cls, tag: str, label: Optional[str] = None, embedding: Optional[np.ndarray] = None) -> 'Spinor':
        components = [cls.from_label(tag)]
        if label:
            components.append(cls.from_label(label))
        if embedding is not None:
            components.append(cls.from_embedding(embedding))
        return cls.bind_all(components)
