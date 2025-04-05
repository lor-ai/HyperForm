# hyperflow.py 

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from spinor import Spinor

# === HyperFlow ===
@dataclass
class HyperFlow:
    init_svsa: Spinor = field(default_factory=lambda: Spinor.encode_init("hyperflow"))
    init_data: Optional[Dict[str, Any]] = field(default_factory=dict)
    orig_svsa: Optional[Spinor] = None
    static_svsa: Optional[Spinor] = None
    dynamic_svsa: Optional[Spinor] = None
    active_svsa: Optional[Spinor] = None

    metadata: Dict[str, Any] = field(default_factory=dict)
    connections: Dict[str, List[str]] = field(default_factory=lambda: {"heads": [], "tails": []})
    transform_rules: Optional[Dict[str, Any]] = field(default_factory=dict)
    visit_count: int = 0
    mass: float = 1.0

    def initialize(self, manifold_svsa: Spinor):
        self.orig_svsa = manifold_svsa
        self.static_svsa = self.init_svsa.bind(manifold_svsa)

    def visit(self, context_svsa: Spinor, manifold_svsa: Optional[Spinor] = None):
        self.visit_count += 1

        context = context_svsa
        if manifold_svsa:
            context = context_svsa.bind(manifold_svsa)

        if self.active_svsa:
            self.active_svsa = self.active_svsa.rotate(context)
        else:
            self.active_svsa = context

        self.dynamic_svsa = self.active_svsa.bind(self.static_svsa)
        return self

    def connect(self, target_id: str, direction: str = "tail"):
        if direction == "head":
            self.connections["heads"].append(target_id)
        else:
            self.connections["tails"].append(target_id)

    def encode_state(self, semantic: str, embedding: Any):
        self.init_data = {
            "text": semantic,
            "embedding": embedding
        }

    def __repr__(self):
        return f"<HyperFlow visits:{self.visit_count} mass:{self.mass}>"
