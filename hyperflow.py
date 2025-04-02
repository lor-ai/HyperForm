# hyperflow.py 

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
import uuid
import numpy as np
from typing import Union

class Spinor:
    def __init__(self, vector: Union[list, np.ndarray]):
        self.vector = np.array(vector, dtype=np.float32)

    def rotate(self, other: 'Spinor') -> 'Spinor':
        # Placeholder for phase alignment logic (to be replaced with SU(2)/SU(N) ops)
        return Spinor(np.add(self.vector, other.vector))

    def bind(self, other: 'Spinor') -> 'Spinor':
        # Superposition or HRR-style binding
        return Spinor(np.multiply(self.vector, other.vector))

    def similarity(self, other: 'Spinor') -> float:
        # Cosine similarity
        norm_self = np.linalg.norm(self.vector)
        norm_other = np.linalg.norm(other.vector)
        if norm_self == 0 or norm_other == 0:
            return 0.0
        return float(np.dot(self.vector, other.vector) / (norm_self * norm_other))

    def permute(self) -> 'Spinor':
        # Placeholder permutation (acts like a symmetry transform)
        return Spinor(np.roll(self.vector, 1))

    def __repr__(self):
        return f"Spinor({self.vector[:5]}...)"

# === HyperFlow ===
@dataclass
class HyperFlow:
    static_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    dynamic_id: Optional[str] = None
    state_vector: Optional[Dict[str, Any]] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    connections: Dict[str, List[str]] = field(default_factory=lambda: {"heads": [], "tails": []})
    transform_rules: Optional[Dict[str, Any]] = field(default_factory=dict)
    spinor_embedding: Optional[Spinor] = None
    visit_count: int = 0
    mass: float = 1.0  # Base mass for traversal cost, evolves with surprise/usage

    def visit(self, context_spinor: Spinor):
        self.visit_count += 1
        self.dynamic_id = str(uuid.uuid4())
        if self.spinor_embedding:
            self.spinor_embedding = self.spinor_embedding.rotate(context_spinor)
        else:
            self.spinor_embedding = context_spinor
        return self

    def connect(self, target_id: str, direction: str = "tail"):
        if direction == "head":
            self.connections["heads"].append(target_id)
        else:
            self.connections["tails"].append(target_id)

    def encode_state(self, semantic: str, embedding: Any):
        self.state_vector = {
            "text": semantic,
            "embedding": embedding
        }

    def __repr__(self):
        return f"<HyperFlow {self.static_id[:8]} visits:{self.visit_count} mass:{self.mass}>"
